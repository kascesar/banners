"""
10_background.py — slide_bg: color sólido, gradiente e imagen de fondo.
Run with: uv run marimo edit test/10_background.py
"""

import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    from banners import configure, Background
    from banners.slides import Cover, Intro, Section, Closing
    from banners.content import Text, Image
    from banners.palette import BLUE, GREEN, PURPLE

    configure(team="Analytics Team", date="April 2026")
    return Background, Closing, Cover, Image, Intro, PURPLE, Section, Text, mo


@app.cell
def _(mo):
    mo.md(r"""
    # `slide_bg` — Fondo por diapositiva

    El parámetro `slide_bg` acepta un objeto `Background` que pinta el fondo
    del contenedor completo del slide (banner + contenido).

    ```python
    from banners import Background

    Cover(title="Demo", slide_bg=Background.color("#0f172a"))
    Cover(title="Demo", slide_bg=Background.gradient("#0d1b2a", "#4a1a6e"))
    Cover(title="Demo", slide_bg=Background.image("assets/photo.jpg"))
    ```

    ## Tres modos

    | Método | Parámetros clave |
    |--------|-----------------|
    | `Background.color(c)` | color CSS: hex, rgb, nombre |
    | `Background.gradient(start, end, *, mid, angle)` | 2 o 3 stops, ángulo en grados |
    | `Background.image(src, *, overlay)` | path / URL / bytes; overlay rgba |
    """)
    return


@app.cell
def _(Image, Text):
    IMAGE_PATH = "img/test.jpeg"
    IMAGE_TEST = {"src":"img/test.jpeg", "size":"10px"}
    content=[
        Text("""
    # Mox aequora luctu coniunx

    ## Rursus posuit nunc procul

    Lorem markdownum. Dedisses tela haec?

    > Pressoque meae, quattuor cura, et corpus ora anus pro aethere florem, dubitas
    > norat volitare vidisti. Hoc aut veteres: qua dederas ensis `dslOop` causa
    > canis *disque*, alter.

    ## Arida quaedam nam super

    Solis vellet munera; de qui pinguescere, esse terris vomit aequore cuius:
    reflectitur. Comes reddidit *me loca* durior, visu viae! Turbatusque aurae
    exsaturanda ab edere ille, pro sed honores, praemia in virgo ad suo aequus
    `wddmBigFile` integer ursa, timore. Inquit qua egit id haesisse tabellis tamen
    iracunda, violentaque addidit ad divino cernunt belua, quandocumque alti.

    In tactas. Circumque cum totaque, mota Medea deus Agenorides meritam piceae
    dumque funduntque? Ubi si nomen, addiderat muros flumina solvit; deam ingentia
    coniunx efficiens cornibus pede. Opem Pan exceptas nec tantus et vellera
    anguicomae intacta: ut leni Lampetide maximus?

    ## Quod Anaxaretes id cultu

    Et unum ille urbe. Aera hausit fonti adfuit memorabile *parvo venitque* vel; non
    Et rorant admonitus. Certamine te marcida per diva medios, qui templi siquis
    corpusque cum.

    ## Fluunt Iuppiter ictus exspectata

    Sonat et freta domumque ostendens blandis, est pariterque potiturque doleam et
    proles. Patris rigidas libertas coniunx. Patria `debuggerStorageSpool` articulos
    iste mentem vocant; sui aura frustraque obruor, priameia, adclivis, *perfundit
    saxo* pariterque.

        bridge.soundOpen.aiff_login(staticTftDpi);
        var cdnCore = twitter(search_flood * matrix + dslamUnit);
        if (host_webcam_remote == chipset_sidebar(core_malware(waveform),
                crop_lpi_plain)) {
            basebandOnlyUser -= logPrinter;
            type_piracy_thunderbolt.iso(3);
        }
        var led = signatureMegabitMnemonic;

    ## Grata debita sed Nioben

    Vana sequuntur necetur rabie `drive` quoque semper inmotos, et dum percussae
    superque Orphei referens, a. Nostrae fratribus puppe: tu solebat dextra
    terebrata totas. Precor `hddLaserVisual` cursus Autumnus Tydides fluere, nos
    Nyctimene ferunt. Factum bracchia tempus. Ad meosque tantum: sidera collo.

        if (10) {
            fileHardeningIpx = ping(burn_dvd, raster, 1);
            twain_processor /= hard;
        }
        var cyclePum = system_copyright;
        card = webmasterScrolling(net_disk(htmlAdMedia + 26,
                horizontal_java_multicasting, hit), agp.phishing(1,
                memory_macro_trackback, copy_syn), mode / ssidDriveToolbar + 3);

        """),
        Image(IMAGE_PATH)
    ]
    return IMAGE_PATH, content


@app.cell
def _(mo):
    mo.md("""
    ## Color sólido
    """)
    return


@app.cell
def _(Background, Cover, content):
    Cover(
        title="Color sólido",
        subtitle="slide_bg=Background.color('#0f172a')",
        slide_bg=Background.color("#0f172a"),
        content=content
    ).render()
    return


@app.cell
def _(Background, Section, content):
    Section(
        title="Color sólido en Section",
        subtitle="Fondo oscuro neutro",
        slide_bg=Background.color("#111827"),
        content=content,
        content_kind="success"
    ).render()
    return


@app.cell
def _(mo):
    mo.md("""
    ## Gradiente personalizado
    """)
    return


@app.cell
def _(Background, Cover, content):
    Cover(
        title="Gradiente 2 colores",
        subtitle="angle=135 (default)",
        slide_bg=Background.gradient("#0d1b2a", "#4a1a6e"),
        content=content,
    ).render()
    return


@app.cell
def _(Background, Intro, content):
    Intro(
        title="Gradiente 3 colores",
        subtitle="Con mid-stop a 50%",
        slide_bg=Background.gradient("#0d1b2a", "#1b4332", mid="#1a3a2a", angle=45),
        content=content,
    ).render()
    return


@app.cell
def _(Background, Section, content):
    Section(
        title="Gradiente horizontal",
        subtitle="angle=90",
        slide_bg=Background.gradient("#1a0533", "#0d1b4a", angle=90),
        content=content,
    ).render()
    return


@app.cell
def _(mo):
    mo.md("""
    ## Imagen de fondo
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    > Para probar con imagen local, reemplaza `IMAGE_PATH` con la ruta a un archivo
    > `.jpg` o `.png` en tu sistema.
    """)
    return


@app.cell
def _(Background, Cover, IMAGE_PATH, content):

    Cover(
        title="Imagen local",
        subtitle="Overlay por defecto: rgba(0,0,0,0.55)",
        slide_bg=Background.image(IMAGE_PATH),
        content=content,
    ).render()
    return


@app.cell
def _(Background, Cover, IMAGE_PATH, content):
    Cover(
        title="Imagen — overlay más oscuro",
        subtitle="overlay='rgba(.5,0,.5,0.2)'",
        slide_bg=Background.image(IMAGE_PATH, overlay="rgba(.5,0,.5,0.2)"),
        content=content
    ).render()
    return


@app.cell
def _(Background, Closing, IMAGE_PATH, content):
    Closing(
        title="Sin overlay",
        subtitle="overlay=None — imagen a full",
        slide_bg=Background.image(IMAGE_PATH, overlay=None),
        content=content,
    ).render()
    return


@app.cell
def _(mo):
    mo.md("""
    ## Sin `slide_bg` — sin regresión
    """)
    return


@app.cell
def _(Cover, PURPLE, content):
    Cover(
        title="Palette por defecto",
        subtitle="Sin slide_bg — usa palette normal",
        palette=PURPLE,
        content=content,
    ).render()
    return


@app.cell
def _(Background, Section, content):
    Section(
        title="Section sin slide_bg",
        subtitle="Comportamiento original sin cambios",
        content=content,
        slide_bg=Background.color("#B3AFC7")
    ).render()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
