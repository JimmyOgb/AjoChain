# AjoChain (AjoBook) 📓⛓️
### Non-Custodial Rotational Savings on X Layer & TapeOut Protocol

> **"One exercise book. Zero collector pockets."**  
> AjoChain keeps the Ajo / Esusu circle exactly as people know it—except the book is an immutable smart contract on X Layer. Every payment is written where everyone can read it, and the contract pays the pot out itself. Nobody holds the money.

---

## 🌟 Live Links & Core Resources

- 🌐 **Live Vercel Production dApp:** **[https://ajochain-mu.vercel.app](https://ajochain-mu.vercel.app)**
- 🎥 **Narrated 1080p Live Demo Video:** **[`demo/ajochain-demo.mp4`](demo/ajochain-demo.mp4)** *(1920x1080, 30fps, 2m 05s, Authentic Nigerian English Narration via `en-NG-AbeoNeural`)*
- 💻 **GitHub Repository:** **[https://github.com/JimmyOgb/AjoChain](https://github.com/JimmyOgb/AjoChain)**
- 🏭 **AjoFactory on OKLink:** **[`0xAD74798cDb9513d06c0060Bf6850a8080F024B0b`](https://www.oklink.com/x-layer-testnet/address/0xAD74798cDb9513d06c0060Bf6850a8080F024B0b)**
- 🔗 **Seed AjoCircle on OKLink:** **[`0xEc454C6f3d5D68Ff310aBeC3b4a6A769aD4D3A6c`](https://www.oklink.com/x-layer-testnet/address/0xEc454C6f3d5D68Ff310aBeC3b4a6A769aD4D3A6c)**
- 🔗 **Verified Live 5-Minute Demo Circle on OKLink:** **[`0x4c2d10851889cf992e4b6a8e12508dcdc11e1642`](https://www.oklink.com/x-layer-testnet/address/0x4c2d10851889cf992e4b6a8e12508dcdc11e1642)**

---

## 📖 The "Exercise Book" User Experience (Zero Human Middlemen)

AjoChain mirrors the exact communal routine of an African market Ajo/Esusu exercise book while eliminating every point of human theft, default, or stalled payouts:

### Step 1 — Host Opens a Circle (`CreateCircleModal`)
- **Circle Name:** Human title for the book (e.g., *"Lagos Tech Founders Ajo"*).
- **Host's Own Name:** The host enters their chosen name (e.g., *"Tunde (Host)"*) and automatically signs their name into Turn #1 in the book.
- **Contribution Amount:** Denominated cleanly in `USDT` (e.g., `10 USDT` or `100 USDT`).
- **Turn Cadence (How Often):**
  - `Every 5 minutes (Live Demo Mode)` (300 seconds for lightning-fast judge evaluations)
  - `Daily` (24 hours)
  - `Weekly` (7 days)
  - `Monthly` (30 days)
- **Require 1-Contribution Deposit:** Toggle for 1x deposit escrow protecting the collector against missed turns.
- **Keep Circle Open for Late Joiners:** Toggle enabling mathematical catch-up for latecomers.

### Step 2 — Join by Link or QR Code
- Every exercise book generates an instant shareable invite URL (`https://ajochain-mu.vercel.app/?circle=0x...`) with a clean inline SVG QR code.
- Anyone scanning or opening the link connects their OKX / Injected wallet, types their **own human name** into the book (e.g., *"Ada"*, *"Chidi"*, *"Ngozi"*), and joins in order (receiving the exact payout turn corresponding to their sign-up position).

### Step 3 — Host Starts & Full-Period Escrowed Turn Payments
- As soon as $\ge 2$ members sign the book, the host clicks **Start Circle** (or it starts automatically when full).
- Each turn, each member pays their contribution with **one single signature**.
- **Full-Period Escrow:** Contributions are held in non-custodial contract escrow for the entire turn period (`turnDeadline = turnStartTime + turnDuration`). The accumulating pot is displayed live.
- Once the scheduled period finishes (`block.timestamp >= turnDeadline`), anyone can call **Release Scheduled Payout** (`releaseTurnPayout` / `closeTurn`):
  - Missing members with deposit coverage have their deposit automatically deducted into the pot.
  - The entire escrowed pot is disbursed to the scheduled turn collector, and the next turn timer begins.

### Step 4 — Edge-Case Safeguards Built Directly Into the Book UI
- 🛡️ **Deposits (1x Contribution Escrow):** Shows each member's locked 1-contribution deposit (`10 USDT` / `100 USDT`). If a member misses a turn, their deposit covers their share so the collector still receives the full pot on time. Unused deposits return automatically at the end of the circle.
- ⏰ **Late Turns (`Close Turn`):** Once a turn's deadline passes, anyone can click **Close Turn**. Unpaid members without deposit coverage are permanently recorded in red as **"Missed"** in the exercise book for everyone to see.
- 🤝 **Joining Late (`Join Late`):** While open, newcomers can join an active running circle at the end of the order by paying a fair catch-up:
  $$\text{Catch-Up} = (T_{\text{current}} - 1) \times \text{Contribution}$$
  This catch-up is split automatically into the vaults of all members who collected before them, ensuring mathematical parity where everyone ends 100% square.
- 💰 **No Stuck Money (`Collect Waiting Funds`):** Any funds the contract could not deliver directly (including late-join catch-up shares) wait safely in the on-chain vault under that member's name until they click **Collect Waiting Funds**.
- 📜 **The Book's History (Real Event Log):** Chronological, line-by-line ledger showing every action (`Opened circle`, `Signed name into book`, `Paid Turn #1`, `Pot delivered`, `Marked Missed`, `Joined late with catch-up`), each hyperlinked directly to its transaction hash on **OKLink X Layer Explorer**.

---

## ⚡ Network-Aware Contract Resolution (Chain Mismatch Prevention)

To guarantee a frictionless experience and eliminate `AbiDecodingZeroDataError` or `0x` empty contract returns:
- **Default Primary Network:** The dApp defaults to **X Layer Testnet (Chain ID: `1952`)** for all unauthenticated visitors and initial page loads (`chains: [xLayerTestnet, xLayerMainnet]`).
- **Reliable Direct RPC Transports:** Connects directly to `https://testrpc.xlayer.tech` (`1952`) and `https://rpc.xlayer.tech` (`196`), eliminating connection-reset errors.
- **Smart Bytecode & Chain Check:** Before calling `getAllCircles()` or reading contract state, the app checks contract bytecode via `publicClient.getBytecode`. If the user's wallet is on X Layer Mainnet (`196`) or another network, a prominent 1-click **"Switch Wallet to X Layer Testnet (1952)"** banner guides the user smoothly.

---

## 🌟 Executive Summary & Problem Statement

### The Problem: The Human Collector Dilemma
Across Nigeria and West Africa, over **$15B+** circulates through informal rotational savings groups (**Ajo** or **Esusu**). A trusted organizer carries a physical **Exercise Book**, collecting daily or weekly contributions and handing the entire pot to one rotating member per turn.

This traditional system breaks down at two critical failure points:
1. **The Runaway Collector:** The organizer holds everyone's cash. Fraud, bank freezes, or theft wipe out entire communities with zero recourse.
2. **Early-Slot Defaulters & Delayed Turns:** A member collects the lump sum in Turn #1 or #2, then defaults or delays payment in Turn #4, stranding later participants.

### The Solution: AjoChain (AjoBook)
AjoChain replaces the vulnerable human collector with an immutable smart contract and TapeOut logic circuit, while preserving the exact communal familiarity of the **Ajo Exercise Book**:
- **Names, Not Just Hashes:** Members sign their human names (*"Chidi"*, *"Ngozi"*, *"Tunde"*) into the on-chain ledger alongside their wallet addresses.
- **Zero-Human Custody:** No admin keys, no pause functions, no upgrade proxies, and no owner backdoors. Funds move exclusively through verified turn payouts, deposit refunds, or late-join distributions.
- **1x Flat Security Deposit:** Protects against missed turns. If a participant misses a contribution, closing the turn automatically deducts the required amount from their deposit, marks their book record as `MISSED`, and releases the pot to the scheduled collector on time.
- **Late-Join Catch-Up:** Newcomers can join an active circle at Turn $T$ by paying the catch-up balance:
  $$\text{Catch-Up} = (T - 1) \times \text{Contribution}$$
  The contract immediately distributes $1 \times \text{Contribution}$ into the `claimableBalance` vault of every past collector ($1 \dots T-1$). No funds are ever stuck.
- **Flexible Turn Cadence:** Instant live demos via **5-minute turns (`300s`)**, as well as Daily (`86400s`), Weekly (`604800s`), and Monthly (`2592000s`) schedules.

---

## 🚀 Live X Layer Testnet Deployments (Proof of Life)

All contracts are deployed live, verified, and operational on **X Layer Testnet (Chain ID: `1952`)**.

| Contract | Address on X Layer Testnet | OKLink Block Explorer |
| :--- | :--- | :--- |
| **AjoFactory** (Upgraded Escrow Timed) | `0xAD74798cDb9513d06c0060Bf6850a8080F024B0b` | [View on OKLink](https://www.oklink.com/x-layer-testnet/address/0xAD74798cDb9513d06c0060Bf6850a8080F024B0b) |
| **Seed AjoCircle** (*Lagos Founders Ajo*) | `0xEc454C6f3d5D68Ff310aBeC3b4a6A769aD4D3A6c` | [View on OKLink](https://www.oklink.com/x-layer-testnet/address/0xEc454C6f3d5D68Ff310aBeC3b4a6A769aD4D3A6c) |
| **TestUSDT** (6-Dec Faucet) | `0xBA2F34E38056aFEc0ab39BD48a0688f4c3680840` | [View on OKLink](https://www.oklink.com/x-layer-testnet/address/0xBA2F34E38056aFEc0ab39BD48a0688f4c3680840) |
| **Verified Live Demo Circle** (*Live Verification Circle*) | `0x4c2d10851889cf992e4b6a8e12508dcdc11e1642` | [View on OKLink](https://www.oklink.com/x-layer-testnet/address/0x4c2d10851889cf992e4b6a8e12508dcdc11e1642) |

### Complete Live On-Chain Lifecycle Proofs (Ada, Chidi, Ngozi)

Executed live on-chain with zero simulations against circle `0x4c2d10851889cf992e4b6a8e12508dcdc11e1642`:

| # | Action | Transaction Hash | OKLink Explorer Link | Verified State & Invariant Result |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **Create Circle** | `0x75b3c10c...` | [View Tx](https://www.oklink.com/x-layer-testnet/tx/0x75b3c10c7c8845f1f70d6f91f970e5c32d7ea32814c9491cf189d3495b96b969) | Deployed 5-minute circle with `10 USDT` turns |
| **2** | **Ada Joins (Slot 1)** | `0x7ecfea5f...` | [View Tx](https://www.oklink.com/x-layer-testnet/tx/0x7ecfea5fd17ba8ac2407302065cb25b855a4eb800a3347176df0c7bd957e832c) | Signed *"Ada"*, Slot #1 assigned, `10 USDT` deposit locked |
| **3** | **Chidi Joins (Slot 2)** | `0x5e129182...` | [View Tx](https://www.oklink.com/x-layer-testnet/tx/0x5e12918217263cef9f62b33d93662d679bee0767ed245b8c72f73dbd2d776fc0) | Signed *"Chidi"*, Slot #2 assigned, `10 USDT` deposit locked |
| **4** | **Host Starts Circle** | `0x9f674cc6...` | [View Tx](https://www.oklink.com/x-layer-testnet/tx/0x9f674cc66fd4367328c987bfdf9583712b8a5b5124649de96b84a265a9fddf77) | Circle transitioned to `ACTIVE`, Turn #1 began |
| **5** | **Ada Contributes** | `0x2462cd00...` | [View Tx](https://www.oklink.com/x-layer-testnet/tx/0x2462cd00670f32bbc6f1ba4bddc93f475e7808a48bf1014180dd08729679204b) | Contributed `10 USDT` for Turn 1 |
| **6** | **Chidi Contributes & Auto-Payout** | `0x56524848...` | [View Tx](https://www.oklink.com/x-layer-testnet/tx/0x56524848b052e30442a3a55c351a4ebf99a9f909132a30001e693508da9df8c0) | **`19.90 USDT` net pot automatically paid to Ada**; Turn #2 started |
| **7** | **Ngozi Joins Late** | `0x932c55b7...` | [View Tx](https://www.oklink.com/x-layer-testnet/tx/0x932c55b75c73d8f723ef8bd63854f813f547b1fd983e3161442f9cb7079d8f69) | Paid `10 USDT` deposit + `10 USDT` catch-up; **Ada credited `10 USDT`** |
| **8** | **Ada Claims Catch-Up** | `0xd939899f...` | [View Tx](https://www.oklink.com/x-layer-testnet/tx/0xd939899f790b513a85764a940833003b8bf66aab5cb2d2c7518691560e26dfba) | Ada withdrew `10 USDT` catch-up balance; vault updated |

---

## 🏗️ Architecture & TapeOut Protocol Integration

```
               +--------------------------------------------------------+
               |                  AjoChain Architecture                 |
               +--------------------------------------------------------+

  [ Savers & OKX Wallet ] 
             |
             v
  +--------------------------------------------------------------------+
  |                     TapeOut DeWEB Static Layer                      |
  |  - Pure Static Bundle (Vite + React + TS, base: './')              |
  |  - Hosted on-chain inside ERC-6551 Circuit Container               |
  |  - TapeKit Dual-RPC Integrity: SHA-256 cross-check on 2 nodes      |
  |    Node 1: https://testrpc.xlayer.tech                             |
  |    Node 2: https://xlayertestrpc.okx.com/terigon                   |
  +--------------------------------------------------------------------+
             |                                    |
             | RPC Reads / Writes                 | TAP-10 Messaging
             v                                    v
  +------------------------------------+  +----------------------------+
  |       X Layer zkEVM Rollup         |  |   TapeSend (TAP-10)        |
  |  - Chain ID: 1952 (Testnet) / 196  |  |  - E2E Encrypted Container |
  |  - Native Gas Token: OKB           |  |    Coordination            |
  |  - Currency: USDT (6 decimals)     |  |  - Turn reminders & alerts |
  |                                    |  +----------------------------+
  |  Contracts:                        |
  |   - AjoFactory.sol                 |
  |   - AjoCircle.sol                  |
  |     - Human Exercise Book Ledger   |
  |     - 1x Security Deposit Escrow   |
  |     - Turn Payout Engine           |
  |     - Late-Join Catch-Up Vault     |
  +------------------------------------+
             |
             v Bound via tapeOutCircuitId & tapeOutProcessor
  +--------------------------------------------------------------------+
  |                     TapeOut Protocol Engine                         |
  |  - Circuit Netlist: AjoPayoutGate (circuit/ajo_payout_gate.json)   |
  |  - Boolean Netlist: NAND & LATCH ERC-1155 Logic Tokens             |
  |  - Circuit NFT: ERC-721 token bound to ERC-6551 Container          |
  |  - Area-coded Container URI: tape://0x89c7d413...2.LAGOS_ARM.tape/ |
  +--------------------------------------------------------------------+
```

### 1. TapeOut Digital Logic Netlist (`AjoPayoutGate`)
In [`circuit/ajo_payout_gate.json`](circuit/ajo_payout_gate.json), AjoChain defines the formal verification logic for payouts and default detection using primitive boolean gates:
- **`releasePayout`**: $\text{allMembersPaid} \land \neg \text{roundAlreadyDisbursed} \land \text{roundActive}$
- **`slashRequired`**: $\text{deadlinePassed} \land \neg \text{memberPaid} \land \text{roundActive}$

### 2. TapeKit Dual-RPC SHA-256 Asset Integrity Check
In [`frontend/src/tapeout/tapekit.ts`](frontend/src/tapeout/tapekit.ts), every loaded bundle computes SHA-256 hashes client-side and validates against both `https://testrpc.xlayer.tech` and `https://xlayertestrpc.okx.com/terigon` to guarantee zero-tamper decentralized hosting.

### 3. TapeSend (TAP-10) Member Coordination
TapeSend provides container-to-container encrypted communication for ROSCA participants (turn opening notices, payout confirmations, deadline countdown alerts) without routing payments or exposing private coordinator chats.

---

## 📐 Mathematical Invariants & Guarantees

1. **Balance Conservation:**
   $$\text{Contract USDT Balance} = \sum_{m} \text{Deposit}_m + \sum_{m} \text{TurnContributions}_{\text{current}} + \sum_{u} \text{claimableBalance}_u$$
2. **Late-Join Invariant (No Stuck Money):**
   When member $N$ joins at Turn $T$:
   $$\text{Catch-Up Paid} = (T - 1) \times \text{Contribution}$$
   $$\sum_{t=1}^{T-1} \Delta \text{claimableBalance}_t = (T - 1) \times \text{Contribution}$$
   Every past collector receives their exact share via safe pull-payments.
3. **Turn Payout Formula:**
   $$\text{Gross Pot} = \text{memberCount} \times \text{Contribution}$$
   $$\text{Protocol Fee} = \frac{\text{Gross Pot} \times 50}{10000} \quad (0.5\%)$$
   $$\text{Net Payout} = \text{Gross Pot} - \text{Protocol Fee}$$

---

## 💻 Local Development & Testing

### Prerequisites
- [Foundry](https://getfoundry.sh/) (`forge`, `cast`)
- Node.js 18+ & npm

### Smart Contracts (Foundry)
```bash
cd contracts
forge install
forge test -vvv
```
All 7 comprehensive exercise book tests pass:
- `test_JoinOrderAndDepositLock`: Verifies human name recording and 1x deposit escrow.
- `test_AutoStartAtMaxMembers`: Verifies circle begins automatically when full.
- `test_HostCanStartWithTwoMembers`: Verifies host initiation once $\ge 2$ members sign.
- `test_TurnContributionAndPayout`: Verifies smooth contribution and net pot distribution.
- `test_MissedTurnDeductedFromDeposit`: Verifies auto-deduction and `MISSED` ledger status.
- `test_LateJoinCatchUpDistribution`: Verifies exact mathematical credit to past collectors.
- `test_DepositRefundAtCompletion`: Verifies 100% deposit returns upon circle completion.

### Frontend (DeWEB Compliant)
```bash
cd frontend
npm install
npm run build
npm run preview
```

### Packaging for DeWEB On-Chain Deployment
```bash
powershell -ExecutionPolicy Bypass -File scripts/package-deweb.ps1
# Or on Linux/macOS:
./scripts/package-deweb.sh
```
Outputs `frontend/dist/deweb-manifest.json` and `ajochain-deweb-bundle.zip`.

---

## 🏆 Hackathon Checklist

- [x] Tested & Deployed on **X Layer** (Chain ID: `1952` Testnet, fully configured for `196` Mainnet).
- [x] Zero-Mock / Zero-Simulation policy strictly adhered to (all UI driven by real RPC calls).
- [x] TapeOut Protocol netlist compiled in `circuit/ajo_payout_gate.json`.
- [x] TapeKit dual-RPC SHA-256 integrity verifier operational.
- [x] 100% On-Chain DeWEB compatible static build (`base: './'`).
- [x] Human Exercise Book interface with Nigerian cultural UX, shareable invite links, and QR codes.
- [x] Complete test coverage with Foundry.

---

## 📄 License
MIT License. Built for the **X Layer & TapeOut Hackathon**.
