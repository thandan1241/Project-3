[V1 | Slide 1 — Title]
Welcome to this Flow Matching tutorial, made by Team 4. We'll build up a complete understanding of flow matching — from core intuition to advanced design choices.
[V1 | Slide 2 — Basics]
Let's start with the basics: what is flow matching, and why does it matter?
[V1 | Slide 3 — Applications]
Flow matching powers some of today's most impressive generative models — Meta's Movie Gen for text-to-video, Stable Diffusion 3 for text-to-image, protein generation, and robot action models. It's a broadly applicable framework.
[V1 | Slide 4 — What is Flow Matching?]
Flow matching is a scalable method to train flow-based generative models. You train a neural network by regressing a velocity field, then generate samples by following that velocity over time — essentially solving a differential equation.
[V1 | Slides 5–6—The Big Picture]
We transform a simple source distribution p — usually Gaussian — into a target data distribution q by learning a flow. Classical normalizing flows do this too, but require unstable training. Flow matching solves this cleanly.
[V1 | Slides 7–9 — Why Flows?]
Generative models can use Flows, Diffusions, or Jump processes. Flows are simpler — faster to sample, support exact likelihoods, and easier to build on. Broadcasts have a larger design space but are slower and use approximate objectives.
[V1 | Slides 10–18—Flow, Velocity, and Sampling]
A flow psi-t maps source sample X-0 to Xt over time. The velocity ut drives this — linked by ODE integration and differentiation. The simplest choice is the linear flow: At inference, draw X-0 from p and integrate the ODE with Euler or Midpoint methods.
[V1 | Slides 19–31 — Why CFM Works + Path Choices]
Flow matching works for any source p, target q, and coupling. The marginal velocity is the conditional expectation of ut given X-1 at Xt — the Marginalization Theorem. The Flow Matching loss is intractable, but the Conditional Flow Matching loss — regressing onto ut given X-1 — has identical gradients. We always train with the conditional loss. For path design, conditional OT paths minimize kinetic energy and give straighter trajectories. Affine paths alpha-t X-1 plus sigma-t X-0 unify many methods; with a Gaussian source they recover noise prediction and data prediction from diffusion models.
[V1 | Slide 32–33 — Advanced Designs]
We now cover three advanced design topics: Conditioning & Guidance, Data Couplings, and Geometric Flow Matching.
[V1 | Slides 34–41 — Conditioning and Guidance]
For conditional generation, we simply give the label Y as an extra input to the velocity network, and train the same CFM loss across all conditions. At inference, if no conditional model was trained, guidance can steer an unconditional model — by modifying the velocity using a classifier gradient. This is how systems like Movie Gen generate rich, text-controlled videos.
[V1 | Slides 42–53 — Paired Data Couplings]
When data comes in pairs — corrupted image and its original — set source X-0 to the corrupted input plus noise. This alters the coupling rather than adding an explicit conditioning signal, letting the model implicitly learn q of x-1 given y. Works naturally for super-resolution and infilling.
[V1 | Slides 54–63 — Multisample Couplings]
For straighter trajectories, optimize the source-target coupling using mini-batch optimal transport. Sample k points from each distribution, solve OT on the mini-batch, then pair samples. k equals 1 gives independent coupling; large k approaches the true OT map. Most useful in low-dimensional scientific settings like protein design.
[V1 | Slides 64–82 — Equivariant Flows]
Molecular data has symmetries — rotations, reflections, permutations. We want invariant density: q of g dot x equals q of x. This requires an equivariant velocity: ut of g dot x equals g times ut of x. Train an equivariant network with the standard CFM loss. Use alignment couplings — align X-1 to X-0 via the symmetry group before pairing — to avoid curved trajectories.
[V1 | Slide 83 — End of Video 1]
Equivariant Flow Matching, by Wu et al., Song et al., and Klein et al., combines equivariant networks with alignment couplings for geometric data. Video 2 goes deeper into Riemannian Flow Matching and model adaptation.

▶ VIDEO 2 — Equivariant Flow Matching & Model Adaptation
Source: fm_tutorial_combined-trang.pptx
[V2 | Slides 1–3—Overview]
Welcome to Part 2, covering flow matching on curved spaces and three post-training techniques: faster sampling, inverse problems, and reward fine-tuning. Key applications: protein generation with SE(3) invariance, SO(2)-invariant robotics, and climate modeling on the sphere.
[V2 | Slides 4–13 — Riemannian Manifolds]
On manifolds, we need to redefine geometric tools. A Riemannian manifold has a metric — an inner product on the tangent space Tx at each point — allowing lengths and angles to be measured on curved surfaces. Velocities must live in the tangent space.
[V2 | Slides 14–19 — Riemannian Flow Matching]
The Riemannian FM loss measures squared error under the Riemannian metric g. A conditional version conditioning on X-1 gives equivalent gradients — so we train with the conditional loss, just as in flat space.
[V2 | Slides 20–24 — Simple Geometries]
For simple manifolds — sphere, torus, hyperbolic — conditional flows follow geodesics via exponential and logarithmic maps: psi-t equals exp at x-0 of kappa-t times log at x-0 of x-1. Closed-form and simulation-free during training.
[V2 | Slides 25–38 — General Geometries]
For general manifolds, use a premetric — a distance-like function — to build flows contracting toward x-1. The velocity has an analytical form via the premetric gradient. Requires ODE simulation during training.
[V2 | Slides 39–41 — vs. Score Matching]
Both Riemannian Flow Matching and Score Matching are simulation-free on simple manifolds. On general manifolds, flow matching uses an ODE while score matching uses an SDE. Flow matching's ODE sampling is typically faster and more stable.
[V2 | Slides 42–61 — Faster Sampling]
Three approaches after training:
Rectified Flows (Liu et al., 2022): reuse the pre-trained coupling to train a new model with straight paths. Enables one-step generation. Small quality drop.
Shortcut Models (Frans et al., 2024): predict large ODE steps with step size h as extra input, trained with Flow Matching plus self-consistency loss. Doesn't support classifier-free guidance.
Bespoke Solvers (Shaul et al., 2023/2024): keep the model fixed, optimize the solver. Transfers across datasets but doesn't match distillation at very low step counts.
[V2 | Slides 62–74—Inverse Problems]
Posterior inference approach : modify the sampling procedure to target p of x-1 given observation y, using a guidance term from the log-likelihood. In practice, the unknown score is replaced by a heuristic approximation using the pseudoinverse of the corruption. Works for linear corruptions with Gaussian paths; can fail randomly.
D-Flow (Ben-Hamu et al., 2024): avoid likelihoods entirely. Use the pre-trained flow as a diffeomorphism — optimize over the source noise x-0 instead of x-1. The flow's Jacobian projects gradients onto the data manifold, allowing mode-hopping. Works with nonlinear corruptions and latent models. Requires differentiating through the ODE.
[V2 | Slides 75–85 — Reward Fine-tuning]
Gradient-based : maximize expected reward using RL or differentiable rewards. Needs LoRA regularization to avoid reward hacking.
Stochastic Optimal Control : target the tilted distribution — base model times exponentiated reward. Naive KL regularization introduces a value function bias. Uehara et al. fix this by learning an optimal source distribution. Adjoint Matching (Domingo-Enrich et al.) uses a memoryless SDE during fine-tuning, then converts back to an ODE for fast deterministic sampling afterward.
[V2 | Slides 86–101 — Generator Matching]
To handle discrete spaces, we use Continuous Time Markov Processes — a framework covering flows, diffusions, and jumps. The generator Lt generalizes velocity to any Markov process. Generator Matching (Holderrieth et al., 2024) trains a network using the same marginalization trick: average conditional generators over X-1 to get the marginal generator.
[V2 | Slides 102–111 — Discrete Flow Matching]
Discrete Flow Matching (Campbell et al. and Gat et al., 2024) applies Generator Matching to token sequences. Velocity is factorized per position: at rate 1 over 1 minus t, jump to the target token. The marginal path mixes data and prior tokens. Demonstrated on a 1.7B code generation model — open challenges remain around factorized velocities and better samplers.
[V2 | Slide 112 — Blueprint]
Every flow matching method follows the same blueprint: choose a coupling, design a path, train by matching conditional velocities, sample by integrating the learned dynamics. This modular view unifies all methods from basic CFM to discrete flows on manifolds.
Thank you for watching. We hope this tutorial gives you a strong foundation to explore flow matching in your own work.