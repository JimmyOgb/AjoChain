import asyncio
import os
import glob
import subprocess
from playwright.async_api import async_playwright

CURSOR_JS = """
(() => {
  if (document.getElementById('demo-cursor')) return;
  const cursor = document.createElement('div');
  cursor.id = 'demo-cursor';
  Object.assign(cursor.style, {
    position: 'fixed', top: '0px', left: '0px',
    width: '24px', height: '24px',
    background: 'rgba(239, 68, 68, 0.9)',
    border: '2.5px solid white', borderRadius: '50%',
    boxShadow: '0 0 16px rgba(0,0,0,0.6)',
    pointerEvents: 'none', zIndex: '9999999',
    transition: 'transform 0.2s cubic-bezier(0.22, 1, 0.36, 1)',
    transform: 'translate(-50%, -50%)'
  });
  document.body.appendChild(cursor);

  document.addEventListener('mousemove', e => {
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';
  });
  document.addEventListener('mousedown', e => {
    cursor.style.transform = 'translate(-50%, -50%) scale(0.65)';
    const ripple = document.createElement('div');
    Object.assign(ripple.style, {
      position: 'fixed', left: e.clientX + 'px', top: e.clientY + 'px',
      width: '12px', height: '12px', borderRadius: '50%',
      border: '3px solid rgba(239, 68, 68, 0.95)',
      transform: 'translate(-50%, -50%) scale(1)',
      opacity: '1', pointerEvents: 'none', zIndex: '9999998',
      transition: 'all 0.45s ease-out'
    });
    document.body.appendChild(ripple);
    requestAnimationFrame(() => {
      ripple.style.transform = 'translate(-50%, -50%) scale(4.5)';
      ripple.style.opacity = '0';
    });
    setTimeout(() => ripple.remove(), 450);
  });
  document.addEventListener('mouseup', () => {
    cursor.style.transform = 'translate(-50%, -50%) scale(1)';
  });
})();
"""

CAPTION_JS = """
(captionText) => {
  let cap = document.getElementById('demo-caption-bar');
  if (!cap) {
    cap = document.createElement('div');
    cap.id = 'demo-caption-bar';
    Object.assign(cap.style, {
      position: 'fixed',
      bottom: '30px',
      left: '100px',
      right: '100px',
      background: 'rgba(11, 18, 32, 0.94)',
      border: '1.5px solid rgba(245, 158, 11, 0.5)',
      borderRadius: '16px',
      padding: '16px 36px',
      color: '#FFFFFF',
      fontSize: '20px',
      fontWeight: '600',
      lineHeight: '1.4',
      textAlign: 'center',
      zIndex: '9999990',
      boxShadow: '0 12px 35px rgba(0,0,0,0.8)',
      backdropFilter: 'blur(12px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '18px',
      transition: 'opacity 0.4s ease'
    });
    document.body.appendChild(cap);
  }
  cap.innerHTML = `<span style="font-size: 26px;">🇳🇬</span><span>"${captionText}"</span>`;
}
"""

async def smooth_move(page, target_x: float, target_y: float, steps: int = 35):
    await page.mouse.move(target_x, target_y, steps=steps)
    await asyncio.sleep(0.15)

async def smooth_click(page, selector: str, pause_after: float = 1.0):
    loc = page.locator(selector).first
    await loc.wait_for(state="visible", timeout=12000)
    await loc.scroll_into_view_if_needed()
    box = await loc.bounding_box()
    if box:
        tx = box["x"] + box["width"] / 2
        ty = box["y"] + box["height"] / 2
        await smooth_move(page, tx, ty, steps=30)
        await asyncio.sleep(0.2)
        await page.mouse.click(tx, ty)
    else:
        await loc.click()
    await asyncio.sleep(pause_after)

async def smooth_type(page, selector: str, text: str, pause_after: float = 0.8):
    await smooth_click(page, selector, pause_after=0.3)
    await page.keyboard.type(text, delay=60)
    await asyncio.sleep(pause_after)

def build_master_audio():
    """
    Combines the 7 audio clips into one master audio track demo/master_audio.mp3
    with exact offsets matching our scene timeline:
      Scene 1: t = 0.5s
      Scene 2: t = 11.0s
      Scene 3: t = 25.0s
      Scene 4: t = 38.0s
      Scene 5: t = 54.0s
      Scene 6: t = 79.0s
      Scene 7: t = 105.0s
    """
    print("Building master audio track...")
    offsets = [0.5, 11.0, 25.0, 38.0, 54.0, 79.0, 105.0]
    inputs = []
    filter_parts = []
    
    for i in range(1, 8):
        inputs.extend(["-i", f"demo/audio/scene{i}.mp3"])
        delay_ms = int(offsets[i-1] * 1000)
        filter_parts.append(f"[{i-1}:a]adelay={delay_ms}|{delay_ms}[a{i}];")
    
    amix_inputs = "".join(f"[a{i}]" for i in range(1, 8))
    filter_str = "".join(filter_parts) + f"{amix_inputs}amix=inputs=7:normalize=0[outa]"
    
    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_str,
        "-map", "[outa]",
        "-c:a", "libmp3lame", "-b:a", "192k",
        "demo/master_audio.mp3"
    ]
    subprocess.run(cmd, check=True)
    
    # check duration
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", "demo/master_audio.mp3"],
        capture_output=True, text=True, check=True
    )
    dur = float(res.stdout.strip())
    print(f"Master audio created: {dur:.2f}s")
    return dur

async def record_demo_video():
    raw_dir = os.path.abspath("demo/raw_video")
    os.makedirs(raw_dir, exist_ok=True)
    for f in glob.glob(os.path.join(raw_dir, "*")):
        try: os.remove(f)
        except: pass

    cinematic_file = os.path.abspath("demo/cinematic_scenes.html").replace("\\", "/")
    cinematic_url = f"file:///{cinematic_file}"
    app_url = "https://ajochain-mu.vercel.app/"
    circle_url = "https://ajochain-mu.vercel.app/?circle=0x4c2d10851889cf992e4b6a8e12508dcdc11e1642"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=raw_dir,
            record_video_size={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        # =====================================================================
        # PART 1: CINEMATIC PROBLEM HOOK (0:00 - 0:37.5)
        # =====================================================================
        print("Starting Part 1 — Cinematic Scenes...")
        await page.goto(cinematic_url, wait_until="domcontentloaded")
        await page.evaluate(CURSOR_JS)
        await smooth_move(page, 960, 540, steps=10)

        # SCENE 1 (t=0.0 to 10.5)
        print("  -> Scene 1: Community Thrift & Heritage (10.5s)")
        await page.evaluate("window.showScene('scene1')")
        await smooth_move(page, 960, 320, steps=25)
        await asyncio.sleep(3.5)
        await smooth_move(page, 640, 680, steps=30)
        await asyncio.sleep(2.5)
        await smooth_move(page, 1280, 680, steps=30)
        await asyncio.sleep(3.5)

        # SCENE 2 (t=10.5 to 24.5)
        print("  -> Scene 2: Fragile Paper Book & Collector Disputes (14.0s)")
        await page.evaluate("window.showScene('scene2')")
        await smooth_move(page, 600, 480, steps=30)
        await asyncio.sleep(3.5)
        await smooth_move(page, 520, 620, steps=25)
        await asyncio.sleep(3.5)
        await smooth_move(page, 1350, 450, steps=30)
        await asyncio.sleep(3.5)
        await smooth_move(page, 1350, 650, steps=25)
        await asyncio.sleep(2.5)

        # SCENE 3 (t=24.5 to 37.5)
        print("  -> Scene 3: Solution Reveal — AjoChain on X Layer & TapeOut (13.0s)")
        await page.evaluate("window.showScene('scene3')")
        await smooth_move(page, 960, 420, steps=30)
        await asyncio.sleep(3.5)
        await smooth_move(page, 450, 720, steps=25)
        await asyncio.sleep(2.5)
        await smooth_move(page, 800, 720, steps=25)
        await asyncio.sleep(2.5)
        await smooth_move(page, 1450, 720, steps=25)
        await asyncio.sleep(3.5)

        # =====================================================================
        # PART 2: LIVE PRODUCTION WALKTHROUGH (0:37.5 - 2:06.5)
        # =====================================================================
        print("Starting Part 2 — Live Walkthrough on https://ajochain-mu.vercel.app/...")
        await page.goto(app_url, wait_until="domcontentloaded")
        await page.wait_for_selector("h1", timeout=15000)
        await page.evaluate(CURSOR_JS)

        # SCENE 4: Hero Banner & Architecture (16.0s, t=37.5 to 53.5)
        print("  -> Scene 4: Hero Banner & 4-Step Architecture (16.0s)")
        await page.evaluate(CAPTION_JS, "Here on X Layer Testnet, AjoChain replaces fragile paper ledgers with immutable on-chain exercise books. The dApp is hosted 100% on-chain via TapeOut DeWEB with zero server dependencies and zero human custody.")
        await smooth_move(page, 960, 260, steps=30)
        await asyncio.sleep(2.5)
        await smooth_move(page, 580, 220, steps=25)
        await asyncio.sleep(2.0)
        
        # Scroll smoothly to 4-step exercise book flow
        for _ in range(3):
            await page.mouse.wheel(0, 160)
            await asyncio.sleep(0.4)
        
        await smooth_move(page, 400, 620, steps=25) # Step 1
        await asyncio.sleep(2.0)
        await smooth_move(page, 720, 620, steps=25) # Step 2
        await asyncio.sleep(2.0)
        await smooth_move(page, 1050, 620, steps=25) # Step 3
        await asyncio.sleep(2.0)
        await smooth_move(page, 1380, 620, steps=25) # Step 4
        await asyncio.sleep(2.0)

        # SCENE 5: Opening a New Exercise Book (25.0s, t=53.5 to 78.5)
        print("  -> Scene 5: Hosting a New Exercise Book Modal (25.0s)")
        await page.evaluate(CAPTION_JS, "Hosting a circle is simple. In Step 1, set the book name, your alias, contribution amount in USDT, and round cadence. Step 2 configures 1x security deposit collateral to prevent defaults. And Step 3 binds the circle to a verifiable TapeOut boolean circuit netlist on X Layer.")
        
        # Scroll up slightly and click "+ Host New Exercise Book"
        await page.mouse.wheel(0, -350)
        await asyncio.sleep(0.6)
        await smooth_click(page, "button:has-text('Host New Exercise Book')", pause_after=1.2)

        # Modal Step 1: fill inputs
        await smooth_type(page, "input[placeholder*='Lagos Tech Founders']", "Abuja Tech Founders Ajo", pause_after=0.5)
        await smooth_type(page, "input[placeholder*='Tunde']", "Amina (Host)", pause_after=0.5)
        
        # Select cadence
        try:
            await page.locator("select").select_option("300")
        except:
            pass
        await asyncio.sleep(0.8)
        
        # Click Next
        await smooth_click(page, "button:has-text('Next')", pause_after=1.5)
        
        # Step 2: Deposit Safeguard
        await smooth_move(page, 960, 520, steps=25)
        await asyncio.sleep(2.0)

        # Click Next
        await smooth_click(page, "button:has-text('Next')", pause_after=1.5)
        
        # Step 3: TapeOut Netlist Binding
        try:
            await smooth_type(page, "input[placeholder*='LAGOS_ARM']", "LAGOS_ARM", pause_after=0.8)
        except:
            pass
        await smooth_move(page, 960, 420, steps=25)
        await asyncio.sleep(2.5)

        # Close Modal
        close_btn = page.locator("button:has(svg.lucide-x)").first
        if await close_btn.count() > 0:
            await smooth_click(page, "button:has(svg.lucide-x)", pause_after=1.5)
        else:
            await page.keyboard.press("Escape")
            await asyncio.sleep(1.5)

        # SCENE 6: Inside the Live Exercise Book (26.0s, t=78.5 to 104.5)
        print("  -> Scene 6: Inside the Live Exercise Book & Safeguards (26.0s)")
        await page.goto(circle_url, wait_until="domcontentloaded")
        await page.wait_for_selector("text=Ada", timeout=15000)
        await page.evaluate(CURSOR_JS)
        await page.evaluate(CAPTION_JS, "Inside our live circle, funds are locked safely in escrow with automatic scheduled payouts. Member turns are tracked in a classic ruled exercise book ledger with live ink stamps: Paid, Missed, or Collecting. 1x deposit protects against defaults, and late joiners can catch up honestly.")
        
        # Smoothly move across the circle title and countdown timer
        await smooth_move(page, 650, 240, steps=30)
        await asyncio.sleep(2.0)
        
        # Open Invite Modal
        await smooth_click(page, "button:has-text('Invite via Link / QR')", pause_after=2.0)
        # Close Invite Modal
        try:
            await smooth_click(page, "button:has(svg.lucide-x)", pause_after=1.2)
        except:
            await page.keyboard.press("Escape")
            await asyncio.sleep(1.2)

        # Highlight ESCROWED IN CONTRACT pot & countdown timer
        await smooth_move(page, 850, 360, steps=30)
        await asyncio.sleep(2.5)

        # Scroll down to Exercise Book Member Ledger
        for _ in range(3):
            await page.mouse.wheel(0, 160)
            await asyncio.sleep(0.4)

        # Hover over Ada (Turn 1, Disbursed)
        await smooth_move(page, 520, 560, steps=25)
        await asyncio.sleep(2.2)
        # Hover over Chidi (Turn 2, COLLECTING NOW)
        await smooth_move(page, 520, 630, steps=25)
        await asyncio.sleep(2.2)
        # Hover over Ngozi (Turn 3, Queued)
        await smooth_move(page, 520, 700, steps=25)
        await asyncio.sleep(2.2)

        # Hover over Late Join Catch-Up Card
        await smooth_move(page, 1420, 520, steps=30)
        await asyncio.sleep(3.0)

        # SCENE 7: On-Chain OKLink Ledger & Closing (22.0s, t=104.5 to 126.5)
        print("  -> Scene 7: On-Chain OKLink Event Ledger & Closing (22.0s)")
        await page.evaluate(CAPTION_JS, "Every contribution, collateral lock, and round payout is permanently audited on the X Layer blockchain. No lost paper, no missing collector. AjoChain: traditional African thrift, powered by zero-knowledge security. Live now at ajochain-mu.vercel.app.")
        
        # Scroll to On-Chain Exercise Book Event History
        for _ in range(4):
            await page.mouse.wheel(0, 180)
            await asyncio.sleep(0.4)

        # Hover over verified OKLink event entries
        await smooth_move(page, 720, 580, steps=25) # Ada Claimed Catch-Up
        await asyncio.sleep(2.0)
        await smooth_move(page, 720, 660, steps=25) # Ngozi Joined Late
        await asyncio.sleep(2.0)
        await smooth_move(page, 720, 740, steps=25) # Turn 1 Disbursed
        await asyncio.sleep(2.5)

        # Grand Closing Title Card (final 7 seconds)
        print("  -> Grand Closing Title Card (7s)")
        await page.goto(cinematic_url, wait_until="domcontentloaded")
        await page.evaluate("window.showScene('scene7_closing')")
        await smooth_move(page, 960, 520, steps=25)
        await asyncio.sleep(6.5)

        # Finalize video
        print("Closing context and saving video stream...")
        video_path = await page.video.path()
        await context.close()
        await browser.close()
        print(f"Playwright video recorded: {video_path}")
        return video_path

def merge_final_video(raw_webm: str):
    print("Merging audio and video with FFmpeg...")
    out_mp4 = os.path.abspath("demo/ajochain-demo.mp4")
    master_audio = os.path.abspath("demo/master_audio.mp3")

    cmd = [
        "ffmpeg", "-y",
        "-i", raw_webm,
        "-i", master_audio,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "20",
        "-r", "30",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        out_mp4
    ]
    subprocess.run(cmd, check=True)
    print(f"Final MP4 generated: {out_mp4}")

    # ffprobe check
    probe_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration,size:stream=width,height,r_frame_rate,codec_name",
        "-of", "default=noprint_wrappers=1",
        out_mp4
    ]
    res = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
    print("\n--- FFPROBE VERIFICATION ---")
    print(res.stdout)

async def main():
    build_master_audio()
    raw_video = await record_demo_video()
    merge_final_video(raw_video)
    print("\nDEMO VIDEO GENERATION COMPLETE!")

if __name__ == "__main__":
    asyncio.run(main())
