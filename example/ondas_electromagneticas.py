"""
ondas_electromagneticas.py — Derivation of EM waves from Maxwell's equations.

Example presentation illustrating the combined use of:
  - Cover / Intro / Section / Closing
  - Text with LaTeX
  - Interactive Manim animation (step-by-step derivation)
  - Plot (matplotlib — visualization of the electric wave)

Run with:
    uv run marimo edit example/ondas_electromagneticas.py
"""

import marimo

__generated_with = "0.23.1"
app = marimo.App(
    width="full",
    layout_file="layouts/ondas_electromagneticas.slides.json",
)


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from banners import configure, Background
    from banners.slides import Cover, Intro, Section, Closing
    from banners.content import Text, Plot, Manim, Image
    from banners.palette import GRAY, ORANGE, BLUE, GREEN

    configure(
        team="Physics — Electromagnetism",
        date="2026",
        palette=ORANGE,
        background=Background.gradient(start="#C0C0C0", end="#FAEDEA", angle=45)
    )
    return (
        Closing,
        Cover,
        Image,
        Intro,
        Manim,
        Plot,
        Section,
        Text,
        mo,
        np,
        plt,
    )


@app.cell
def _(Cover, Text):
    Cover(
        title="Electromagnetic Waves",
        subtitle="Derivation from Maxwell's Equations",
        content=[
            Text("**Maxwell's equations** — the starting point."),
            Text("**Animated derivation** — from curl to wave equation."),
            Text("**The speed of light** — an inevitable consequence."),
        ],
        content_kind="warn"
    ).render()
    return


@app.cell
def _(Intro, Text):
    Intro(
        title="What Are We Going to Prove?",
        subtitle="How four laws of electromagnetism predict the existence of waves.",
        tag="Introduction",
        summary=(
            "In 1865, Maxwell unified electricity and magnetism into four equations. "
            "Combined, they reveal that the E and B fields can propagate as waves in vacuum — "
            "and that the wave travels at exactly the speed of light."
        ),
        content=[
            Text("**Faraday** — a varying E field induces a B field."),
            Text("**Ampère–Maxwell** — a varying B field induces an E field."),
            Text("**Together** — they feed back into each other and produce a wave that propagates without a material medium."),
        ],
        content_kind="info",
    ).render()
    return


@app.cell
def _(Section, Text):
    Section(
        title="Maxwell's Equations",
        subtitle="The four fundamental laws of electromagnetism in vacuum",
        content=[
            Text(r"""
    **I — Gauss's Law (electric)** *(no free charges in vacuum)*

    $$\nabla \cdot \mathbf{E} = 0$$

    **II — Gauss's Law (magnetic)** *(no magnetic monopoles exist)*

    $$\nabla \cdot \mathbf{B} = 0$$

    **III — Faraday's Law** *(varying E field generates B field)*

    $$\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}$$

    **IV — Ampère–Maxwell Law** *(varying B field generates E field)*

    $$\nabla \times \mathbf{B} = \mu_0 \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}$$
    """),
        ],
    ).render()
    return


@app.cell(hide_code=True)
def _(Manim, Section):
    from manim import (
        Scene,
        MathTex,
        Text as MText,
        Write,
        FadeIn,
        FadeOut,
        ReplacementTransform,
        UP,
        DOWN,
        WHITE as MWHITE,
        YELLOW as MYELLOW,
        GREEN as MGREEN,
    )

    class MaxwellDerivationScene(Scene):
        """Step-by-step derivation of the electric wave equation."""

        def construct(self):
            self.camera.background_color = "#0f172a"

            # ── Step 0: starting equations ───────────────────────────────────
            self.next_section("start")

            caption = MText(
                "Starting point — Maxwell's laws III and IV",
                font_size=26, color="#9ca3af",
            ).to_edge(UP, buff=0.4)

            faraday = MathTex(
                r"\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}",
                font_size=44, color=MWHITE,
            ).shift(UP * 0.9)

            ampere = MathTex(
                r"\nabla \times \mathbf{B} = \mu_0 \varepsilon_0"
                r"\frac{\partial \mathbf{E}}{\partial t}",
                font_size=44, color=MWHITE,
            ).shift(DOWN * 0.9)

            self.play(FadeIn(caption))
            self.play(Write(faraday), Write(ampere))
            self.wait(1)

            # ── Step 1: apply ∇× to Faraday ──────────────────────────────────
            self.next_section("curl_faraday")

            self.play(FadeOut(caption), FadeOut(ampere))

            caption2 = MText(
                "Step 1 — Apply ∇× to Faraday's law",
                font_size=26, color="#9ca3af",
            ).to_edge(UP, buff=0.4)

            curl_eq = MathTex(
                r"\nabla \times (\nabla \times \mathbf{E})"
                r"= -\frac{\partial}{\partial t}(\nabla \times \mathbf{B})",
                font_size=36, color=MWHITE,
            )

            self.play(FadeIn(caption2))
            self.play(ReplacementTransform(faraday, curl_eq))
            self.wait(1)

            # ── Step 2: vector identity ───────────────────────────────────────
            self.next_section("vector_identity")

            self.play(FadeOut(caption2))

            caption3 = MText(
                "Step 2 — Identity: ∇×(∇×E) = ∇(∇·E) − ∇²E",
                font_size=24, color="#9ca3af",
            ).to_edge(UP, buff=0.4)

            identity_eq = MathTex(
                r"\nabla(\nabla \cdot \mathbf{E}) - \nabla^2 \mathbf{E}"
                r"= -\frac{\partial}{\partial t}(\nabla \times \mathbf{B})",
                font_size=32, color=MWHITE,
            )

            self.play(FadeIn(caption3))
            self.play(ReplacementTransform(curl_eq, identity_eq))
            self.wait(1)

            # ── Step 3: apply ∇·E = 0 (Gauss) ───────────────────────────────
            self.next_section("electric_gauss")

            self.play(FadeOut(caption3))

            caption4 = MText(
                "Step 3 — Electric Gauss: ∇·E = 0 in vacuum",
                font_size=26, color="#9ca3af",
            ).to_edge(UP, buff=0.4)

            gauss_eq = MathTex(
                r"-\nabla^2 \mathbf{E}"
                r"= -\frac{\partial}{\partial t}(\nabla \times \mathbf{B})",
                font_size=40, color=MWHITE,
            )

            self.play(FadeIn(caption4))
            self.play(ReplacementTransform(identity_eq, gauss_eq))
            self.wait(1)

            # ── Step 4: substitute Ampère–Maxwell law ────────────────────────
            self.next_section("ampere_substitution")

            self.play(FadeOut(caption4))

            caption5 = MText(
                "Step 4 — Substitute ∇×B with the Ampère–Maxwell law",
                font_size=24, color="#9ca3af",
            ).to_edge(UP, buff=0.4)

            ampere_sub = MathTex(
                r"\nabla^2 \mathbf{E}"
                r"= \mu_0 \varepsilon_0 \frac{\partial^2 \mathbf{E}}{\partial t^2}",
                font_size=44, color=MWHITE,
            )

            self.play(FadeIn(caption5))
            self.play(ReplacementTransform(gauss_eq, ampere_sub))
            self.wait(1)

            # ── Result: wave equation ────────────────────────────────────────
            self.next_section("wave_equation")

            self.play(FadeOut(caption5))

            caption6 = MText(
                "Result — Electromagnetic wave equation",
                font_size=26, color=MGREEN,
            ).to_edge(UP, buff=0.4)

            wave_eq = MathTex(
                r"\nabla^2 \mathbf{E} = \frac{1}{c^2}"
                r"\frac{\partial^2 \mathbf{E}}{\partial t^2}",
                font_size=56,
            ).set_color(MYELLOW)

            speed_def = MathTex(
                r"c \;=\; \frac{1}{\sqrt{\mu_0\,\varepsilon_0}}",
                font_size=36, color="#3b82f6",
            ).next_to(wave_eq, DOWN, buff=0.65)

            self.play(FadeIn(caption6))
            self.play(ReplacementTransform(ampere_sub, wave_eq))
            self.play(FadeIn(speed_def))
            self.wait(2)

    Section(
        title="Derivation — Step by Step",
        subtitle="From Maxwell's equations to the wave equation · click to advance",
        content=[
            Manim(
                MaxwellDerivationScene,
                interactive=True,
                quality="medium",
                width="78%",
            ),
        ],
    ).render()
    return


@app.cell(hide_code=True)
def _(Plot, Section, Text, mo, np, plt):
    x = np.linspace(0, 4 * np.pi, 600)
    k = 1.0

    fig, ax = plt.subplots(figsize=(11, 3.8))
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")

    snapshots = [
        (0.0,           r"$t = 0$",    "#3b82f6"),
        (np.pi / 2,     r"$t = T/4$",  "#22c55e"),
        (np.pi,         r"$t = T/2$",  "#f59e0b"),
        (3 * np.pi / 2, r"$t = 3T/4$", "#a855f7"),
    ]

    for t_val, lbl, col in snapshots:
        ax.plot(x, np.sin(k * x - t_val), color=col, linewidth=2.2, label=lbl)

    ax.axhline(0, color="#374151", linewidth=0.8, linestyle="--")
    ax.set_xlabel(r"$x$  [units of $k^{-1}$]", color="#9ca3af", fontsize=11)
    ax.set_ylabel(r"$E(x,\,t)\;/\;E_0$", color="#9ca3af", fontsize=11)
    ax.set_title(
        r"$E(x,t) = E_0 \sin(kx - \omega t)$  —  snapshots at four instants",
        color="white", fontsize=13, pad=10,
    )
    ax.tick_params(colors="#6b7280")
    for spine in ax.spines.values():
        spine.set_color("#374151")
    ax.legend(facecolor="#1f2937", edgecolor="#374151", labelcolor="white", fontsize=10)
    ax.grid(color="#1f2937", linewidth=0.8)
    plt.tight_layout()

    Section(
        title="Solution — Electric Wave",
        subtitle="The wave equation admits sinusoidal solutions that propagate at speed c",
        content=mo.vstack([
            Text(
                r"The general 1D solution is $E(x,t) = E_0 \sin(kx - \omega t)$, "
                r"with dispersion relation $\omega = ck$ and $k = 2\pi/\lambda$."
            ).render(),
            Plot(fig).render(),
        ]),
    ).render()
    return


@app.cell
def _(Section, Text, np):
    mu0    = 4.0 * np.pi * 1e-7        # H/m
    eps0   = 8.854187817e-12           # F/m
    c_calc = 1.0 / np.sqrt(mu0 * eps0) # m/s
    c_ref  = 299_792_458.0             # m/s (exact CODATA value)
    error  = abs(c_calc - c_ref) / c_ref * 100

    Section(
        title="Propagation Speed",
        subtitle="The electromagnetic wave travels at exactly c — the speed of light",
        content=[
            Text(
                r"""
    The phase velocity follows directly from the wave equation:

    $$v = \frac{1}{\sqrt{\mu_0\,\varepsilon_0}}$$

    | Constant | Value | Unit |
    |----------|-------|------|
    | $\mu_0$ | $4\pi \times 10^{-7}$ | H/m |
    | $\varepsilon_0$ | $8.854 \times 10^{-12}$ | F/m |
    | $v = 1/\sqrt{\mu_0\varepsilon_0}$ | **"""
                + f"{c_calc:,.0f}"
                + r"""** | m/s |
    | $c$ (CODATA) | **299 792 458** | m/s |
    | Relative error | **"""
                + f"{error:.1e}"
                + r"""** | — |

    > Maxwell concluded in 1865: *"the velocity of transverse undulations in our hypothetical medium, calculated from the electro-magnetic experiments of MM. Kohlrausch and Weber, agrees so exactly with the velocity of light calculated from the optical experiments of M. Fizeau, that we can scarcely avoid the inference that light consists in the transverse undulations of the same medium."*
    """
            ),
        ],
    )
    return


@app.cell
def _(Closing, Text):
    Closing(
        title="Conclusions",
        subtitle="Maxwell's equations predict — without any additional hypothesis — the existence of electromagnetic waves.",
        content=[
            Text("Laws **III** (Faraday) and **IV** (Ampère–Maxwell) couple together and generate a wave equation."),
            Text("The speed $v = 1/\\sqrt{\\mu_0\\varepsilon_0}$ equals $c$ — light **is** an electromagnetic wave."),
            Text("The solution $E_0\\sin(kx-\\omega t)$ describes transverse waves that propagate without a material medium."),
        ],
        content_kind="warn",
    )
    return


@app.cell
def _(Closing, Image):
    Closing(
        title="Thank you",
        content=[
            Image("https://s2.abcstatics.com/media/bienestar/2019/11/28/dar-gracias-6-k2EB--1248x698@abc.jpg", "50%")
        ],
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
