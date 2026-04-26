function render({ model, el }) {
    const srcs = model.get("srcs");
    let idx = 0;
    let busy = false;

    el.style.cssText = "text-align:center;user-select:none;";

    const wrap = document.createElement("div");
    const maxW = model.get("width") || "100%";
    wrap.style.cssText = "display:block;width:100%;max-width:" + maxW + ";margin:0 auto;";

    const stage = document.createElement("div");
    stage.style.cssText = "position:relative;width:100%;overflow:hidden;border-radius:0.5rem;background:#000;cursor:pointer;";
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
    controls.style.cssText = "display:flex;align-items:center;justify-content:center;gap:1rem;margin-top:0.5rem;";

    function makeBtn(text) {
        const b = document.createElement("button");
        b.textContent = text;
        b.style.cssText = "background:#1f2937;color:#9ca3af;border:1px solid #374151;"
            + "border-radius:0.375rem;padding:0.2rem 0.7rem;cursor:pointer;font-size:0.85rem;";
        return b;
    }

    const btnPrev = makeBtn("←");
    const label = document.createElement("span");
    label.style.cssText = "font-size:0.8rem;color:#9ca3af;min-width:4rem;display:inline-block;";
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
            btnAuto.style.color = "#60a5fa";
            btnAuto.style.borderColor = "#3b82f6";
            if (buf[0].ended) { goForward(); } else { attachAutoEnded(); }
        } else {
            btnAuto.style.color = "#9ca3af";
            btnAuto.style.borderColor = "#374151";
        }
    });

    wrap.appendChild(controls);
    el.appendChild(wrap);

    // Apply initial autoplay state
    if (autoplay) {
        btnAuto.style.color = "#60a5fa";
        btnAuto.style.borderColor = "#3b82f6";
        attachAutoEnded();
    }
}
export default { render };
