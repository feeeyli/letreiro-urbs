<script lang="ts">
    import { Canvas } from "svelte-canvas";
    import Led from "./components/Led.svelte";
    import { onMount } from "svelte";
    import DATA from "./lib/data.json";

    type Display = {
        name: string;
        data: number[][];
    };

    const entries = Object.entries(DATA) as [string, Display[]][];
    const displays = entries[
        Math.floor(Math.random() * entries.length)
    ][1] as Display[];

    let index = 0;
    let clear: number;
    let moveInterval: number;
    let moveX = $state(0);

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

    const pallete = ["#232428", "#ffffff", "#ffaa24"];

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
</script>

<div class="container">
    {#if shifted.length > 0}
        <Canvas height={13 * 6} width={shifted.length * 6}>
            {#each { length: shifted[0].length }, y}
                {#each { length: shifted.length }, x}
                    <Led {x} {y} fill={pallete[shifted[x][y]]} />
                {/each}
            {/each}
        </Canvas>
    {/if}
</div>

<style>
    .container {
        width: 100%;
        height: 100%;
        background-color: #292a2f;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 16px;
    }
</style>
