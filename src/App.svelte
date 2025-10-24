<script lang="ts">
    import { Canvas } from "svelte-canvas";
    import Led from "./components/Led.svelte";
    import { onMount } from "svelte";
    import DATA from "./lib/data.json";
    import {
        BG_COLORS,
        COLOR_PALETTE,
        LED_GAP,
        LED_RADIUS,
    } from "./lib/contants";

    type Display = {
        name: string;
        data: number[][];
    };

    const entries = Object.entries(DATA);
    const displayList = entries.map((d) => d[1] as Display[]);
    let displayIndex = $state(Math.floor(Math.random() * displayList.length));
    const displays = $derived(displayList[displayIndex]);

    let index = 0;
    let clear: number;
    let moveInterval: number;
    let moveX = $state(0);

    function cycleIndex<T>(arr: T[], i: number, dir = 1) {
        if (dir > 0) {
            if (i === arr.length - 1) return 0;
            else return i + 1;
        } else {
            if (i === 0) return arr.length - 1;
            else return i - 1;
        }
    }

    onMount(() => {
        clearInterval(clear);
        clear = setInterval(() => {
            if (index === displays.length - 1) index = 0;
            else index += 1;
        }, 2500);

        clearInterval(moveInterval);
        moveInterval = setInterval(() => {
            moveX++;
        }, 100);
    });

    function shiftedArray(arr: Display, amount: number): number[][] {
        if (["hearts"].includes(arr.name)) {
            if (arr.data.length === 0) return [];
            const count =
                ((amount % arr.data.length) + arr.data.length) %
                arr.data.length;
            return [...arr.data.slice(count), ...arr.data.slice(0, count)];
        }

        return arr.data;
    }

    const shifted = $derived(shiftedArray(displays[index], moveX));

    let ledRadius = $state(LED_RADIUS);
    let ledGap = $state(LED_GAP);

    function handleKeyDown(ev: KeyboardEvent) {
        switch (ev.key) {
            case "+":
                if (ledRadius < 15) ledRadius++;
                break;
            case "-":
                if (ledRadius > 2) ledRadius--;
                break;
            case "ArrowRight":
                if (ledGap < 10) ledGap++;
                break;
            case "ArrowLeft":
                if (ledGap > 0) ledGap--;
                break;
            case "ArrowUp":
                index = 0;
                moveX = 0;
                displayIndex = cycleIndex(displayList, displayIndex);
                break;
            case "ArrowDown":
                index = 0;
                moveX = 0;
                displayIndex = cycleIndex(displayList, displayIndex, -1);
                break;
        }
    }
</script>

<svelte:window onkeydown={handleKeyDown} />

<main style:background-color={BG_COLORS[entries[displayIndex][0]]}>
    <div class="container">
        {#if shifted.length > 0}
            <Canvas
                height={13 * (ledRadius * 2 + ledGap)}
                width={shifted.length * (ledRadius * 2 + ledGap)}
            >
                {#each { length: shifted[0].length }, y}
                    {#each { length: shifted.length }, x}
                        <Led
                            {x}
                            {y}
                            fill={COLOR_PALETTE[shifted[x][y]]}
                            {ledRadius}
                            {ledGap}
                        />
                    {/each}
                {/each}
            </Canvas>
        {/if}
        <p class="hint">
            Use <strong>+</strong> ou <strong>-</strong> para mudar o tamanho
            dos leds ({ledRadius}px); <br />
            <strong>seta pra esquerda/direita</strong> para mudar o espaçamento
            ({ledGap}px)
            <br />
            e <strong>seta pra cima/baixo</strong> para trocar o display ({displayIndex +
                1})
        </p>
    </div>
</main>

<style>
    .container {
        width: 100%;
        height: 100%;
        background-color: #292a2f;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 16px;
        padding: 8px;
        overflow: hidden;
    }

    .hint {
        position: absolute;
        bottom: 24px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 14px;
        color: white;
        opacity: 0.15;
        text-align: center;
        cursor: default;
        transition: opacity 250ms ease-in-out;

        &:hover {
            opacity: 0.5;
        }
    }

    main {
        height: 100vh;
        width: 100vw;
        padding: 12px;
    }
</style>
