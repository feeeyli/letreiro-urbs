<script lang="ts">
    import { Layer } from "svelte-canvas";
    import { LED_GAP, LED_RADIUS } from "../lib/contants";

    type Props = {
        x: number;
        y: number;
        fill: string;
        ledRadius: number;
        ledGap: number;
    };

    const {
        x = 0,
        y = 0,
        fill = "black",
        ledRadius = LED_RADIUS,
        ledGap = LED_GAP,
    }: Props = $props();

    function px(n: number) {
        return n * (ledRadius * 2 + ledGap) + ledRadius;
    }

    const render = ({ context }: { context: CanvasRenderingContext2D }) => {
        context.fillStyle = fill;
        context.beginPath();
        context.arc(px(x), px(y), ledRadius, 0, 2 * Math.PI);
        context.fill();
    };
</script>

<Layer {render} />
