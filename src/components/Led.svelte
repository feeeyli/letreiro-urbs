<script lang="ts">
    import { Layer } from "svelte-canvas";

    const { x = 0, y = 0, fill = "black" } = $props();

    function px(n: number) {
        return n * 6 + 2;
    }

    const render = ({ context }: { context: CanvasRenderingContext2D }) => {
        const r = 2;

        context.fillStyle = fill;
        context.beginPath();
        context.arc(px(x), px(y), r, 0, 2 * Math.PI);
        context.fill();
    };
</script>

<Layer {render} />
