# Game-Theoretic Model Intuitive Translation

Technique for translating formal game-theoretic equilibrium conditions into narrative, intuitive explanations that satisfy academic supervisors who demand conceptual clarity alongside mathematical rigor.

## When to use this

- A paper defines a multi-player game (Stackelberg, Nash, etc.) with equilibrium conditions
- The user asks "what assumptions are given?" or "what is the intuition behind Condition X?"
- The user wants to connect a formal model to a real-world research question (RQ)

## Translation template (5-step)

### Step 1: Identify the game structure
Extract from the paper:
- Players and their types (e.g., vendor / white hat / black hat)
- Timing (simultaneous / sequential / multi-stage)
- Information structure (perfect / imperfect / asymmetric)

**Output**: A structural diagram in ASCII or Mermaid, e.g.:
```
Stage 1: Leader chooses (t, p_s, p_ns)
    ↓ observed by followers
Stage 2: Followers simultaneously choose effort (α, β, μ)
    ↓
Outcome: who finds the bug first
```

### Step 2: Decompose the equilibrium effort equation
For each player type, identify:
- `Numerator`: what incentives drive effort (reward, reputation, illicit gain)
- `Denominator`: what suppresses effort (cost multipliers, number of competitors)
- `Residual term`: exogenous state (e.g., K_s(t) = likelihood bug exists)

**Example** (Gal-Or et al. 2024):
```
α_s = [1 / ((n+m) × c_w)] × K_s(t) × (r_s + p_s)
      └─────────────┘   └──────┘   └─────────┘
      competition +     bug       incentives
      cost multiplier   presence  (money + reputation)
```

### Step 3: Translate existence conditions into plain language
Most models have a condition of the form `LB < X < UB`.

Translate each bound into a real-world sentence:
- **Lower bound violation**: "If black hats are too strong (W too high relative to costs), the market collapses because white hats cannot be incentivized"
- **Upper bound violation**: "If white hats already have strong intrinsic motivation (reputation r_s too high), the vendor can reduce monetary rewards"
- **The interval itself**: "The market only functions when the 'net attractiveness of black-hat activity' falls within a moderate range"

**Critical nuance**: Check if the paper says the condition is "necessary and sufficient" or only "sufficient". If the authors admit it is "stronger than necessary", explicitly note this and frame it as a research opportunity.

### Step 4: Connect purpose layers to the model
Many security-economics models have a dual-purpose structure:
1. **Primary purpose**: profit maximization of the market designer (e.g., vendor)
2. **Secondary purpose**: deterrence / externality reduction (e.g., attracting white hats away from black hats)

Use the model to show:
- The secondary effect is **embedded as a strategic interaction**, not the market's declared goal
- The equilibrium condition mathematically encodes the tradeoff between the two purposes

### Step 5: Map to a Research Question
Once the model is intuitively translated, construct an RQ using this template:

> "In [domain], [primary actor]'s [primary objective] and [secondary effect] are formally linked through [equilibrium condition]. Under [new shock / new parameter regime], how does this condition shift, and what are the consequences for [market outcome / ecosystem health / participant behavior]?"

**Example** (this session's RQ):
> "In smart-contract bug bounty markets, the vendor's profit maximization and black-hat deterrence are linked through the BBP existence condition. Under AI-era rule friction (which alters c_w, c_KYC, and p_penalty for low-reputation researchers), how does this condition shift, and what are the consequences for white-hat supply and market concentration?"

## Pitfalls to avoid

- **Do not** present the existence condition as a black-box inequality. Always unpack what each symbol represents in the domain context.
- **Do not** claim a sufficient condition is necessary-and-sufficient unless the paper explicitly proves it.
- **Do not** skip the "secondary purpose" discussion when the user is asking about market definitions — supervisors often challenge whether the secondary effect is truly part of the market's purpose.
- **Do not** use bullet points for the intuitive translation; the user prefers narrative prose with embedded tables.

## Reuse signals

This technique applies to any paper in:
- Security economics (vulnerability markets, bug bounties, cyber-insurance)
- Two-sided platform economics
- Auction / mechanism design with strategic agents
- Any model where a "leader-follower" or "three-player" game structure is used
