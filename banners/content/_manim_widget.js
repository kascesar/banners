function render({ model, el }) {
    const srcs = model.get("srcs");
    // Palette colors from Python: panel behind the video, muted idle controls,
    // primary for the active autoplay toggle.
    const colors = model.get("colors") || { panel: "transparent", muted: "#6b7280", primary: "#e4572e" };
    let idx = 0;
    let busy = false;

    el.style.cssText = "text-align:center;user-select:none;";

    const wrap = document.createElement("div");
    const maxW = model.get("width") || "100%";
    wrap.style.cssText = "display:block;width:100%;max-width:" + maxW + ";margin:0 auto;";

    const stage = document.createElement("div");
    stage.style.cssText = "position:relative;width:100%;overflow:hidden;background:" + colors.panel + ";cursor:pointer;";
    wrap.appendChild(stage);

    function makeVideo() {
        const v = document.createElement("video");
        v.muted = true;
        v.setAttribute("playsinline", "");
        v.loop = false;
        v.style.cssText = "position:absolute;top:0;left:0;width:100%;height:100%;display:block;";
        return v;
    }

    const buf = [makeVideo(), makeVideo()];
    buf[0].style.zIndex = "1";
    buf[1].style.zIndex = "0";
    buf[0].src = srcs[0];
    buf[0].autoplay = true;
    stage.appendChild(buf[0]);
    stage.appendChild(buf[1]);

    buf[0].addEventListener("loadedmetadata", function onMeta() {
        buf[0].removeEventListener("loadedmetadata", onMeta);
        stage.style.aspectRatio = buf[0].videoWidth + " / " + buf[0].videoHeight;
    });

    function whenReady(video, cb) {
        let done = false;
        function fire() {
            if (done) return;
            done = true;
            video.removeEventListener("canplay", fire);
            cb();
        }
        video.addEventListener("canplay", fire);
        if (video.readyState >= 3) fire();
    }

    function preloadNext() {
        const next = idx + 1;
        if (next < srcs.length) { buf[1].src = srcs[next]; buf[1].load(); }
    }
    preloadNext();

    // Controls bar: [←]  "2 / 5"  [→]  [▶]
    const controls = document.createElement("div");
    controls.style.cssText = "display:flex;align-items:center;justify-content:center;gap:1em;margin-top:0.4em;"
        + "background:transparent;color:" + colors.muted + ";";

    function makeBtn(text) {
        const b = document.createElement("button");
        b.textContent = text;
        b.style.cssText = "background:transparent;color:" + colors.muted + ";border:none;"
            + "padding:0.1em 0.4em;cursor:pointer;font-size:0.9em;line-height:1;";
        return b;
    }

    const btnPrev = makeBtn("←");
    const label = document.createElement("span");
    label.style.cssText = "font-size:0.8em;color:" + colors.muted + ";min-width:3.5em;display:inline-block;"
        + "font-variant-numeric:tabular-nums;";
    label.textContent = "1 / " + srcs.length;
    const btnNext = makeBtn("→");
    const btnAuto = makeBtn("▶");
    controls.append(btnPrev, label, btnNext, btnAuto);

    function updateLabel() {
        label.textContent = (idx + 1) + " / " + srcs.length;
    }

    // Autoplay state (may be pre-enabled via model)
    let autoplay = model.get("autoplay");

    function onEnded() {
        if (autoplay) goForward();
    }

    function attachAutoEnded() {
        buf[0].addEventListener("ended", onEnded, { once: true });
    }

    function transition(nextIdx) {
        if (busy) return;
        busy = true;
        idx = nextIdx;
        updateLabel();
        buf[1].src = srcs[idx];
        buf[1].load();
        whenReady(buf[1], function () {
            buf[1].play();
            buf[0].style.zIndex = "0";
            buf[1].style.zIndex = "1";
            buf.reverse();
            busy = false;
            preloadNext();
            if (autoplay) attachAutoEnded();
        });
    }

    function goForward() { transition((idx + 1) % srcs.length); }
    function goBack()    { transition(idx === 0 ? srcs.length - 1 : idx - 1); }

    stage.addEventListener("click", goForward);
    btnNext.addEventListener("click", goForward);
    btnPrev.addEventListener("click", goBack);

    btnAuto.addEventListener("click", function () {
        autoplay = !autoplay;
        if (autoplay) {
            btnAuto.style.color = colors.primary;
            if (buf[0].ended) { goForward(); } else { attachAutoEnded(); }
        } else {
            btnAuto.style.color = colors.muted;
        }
    });

    wrap.appendChild(controls);
    el.appendChild(wrap);

    // Apply initial autoplay state
    if (autoplay) {
        btnAuto.style.color = colors.primary;
        attachAutoEnded();
    }
}
export default { render };
