function render({ model, el }) {
    const color = model.get("color");
    el.innerHTML = model.get("svg");

    el.querySelectorAll(".ag-node").forEach(function(g) {
        g.addEventListener("click", function() {
            const r = g.querySelector("rect");
            const on = g.dataset.hl === "1";
            r.style.fill   = on ? "" : color;
            r.style.filter = on ? "" : "brightness(1.15)";
            g.dataset.hl   = on ? "0" : "1";
        });
    });
}
export default { render };
