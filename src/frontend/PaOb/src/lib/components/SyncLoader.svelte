<script lang="ts">
	import type { SpinnerTypes } from './types/spinner.type';
	import { range, durationUnitRegex } from './utils';
	export let color: SpinnerTypes['color'] = '#FF3E00';
	export let unit: SpinnerTypes['unit'] = 'px';
	export let duration: SpinnerTypes['duration'] = '0.6s';
	export let size: SpinnerTypes['size'] = '60';
	export let pause: SpinnerTypes['pause'] = false;
	let durationUnit: string = duration.match(durationUnitRegex)?.[0] ?? 's';
	let durationNum: string = duration.replace(durationUnitRegex, '');
</script>

<div class="wrapper" style="--size:{size}{unit}; --duration: {duration};">
	{#each range(3, 1) as i}
		<div
			class="dot"
			class:pause-animation={pause}
			style="--dotSize:{+size * 0.25}{unit}; --color:{color}; animation-delay:  {i *
				(+durationNum / 10)}{durationUnit};"></div>
	{/each}
</div>

<style>
	.wrapper {
		height: var(--size);
		width: var(--size);
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.dot {
		height: var(--dotSize);
		width: var(--dotSize);
		background-color: var(--color);
		margin: 2px;
		display: inline-block;
		border-radius: 100%;
		animation: sync var(--duration) ease-in-out infinite alternate both running;
	}
	.pause-animation {
		animation-play-state: paused;
	}

	@-webkit-keyframes sync {
		33% {
			-webkit-transform: translateY(10px);
			transform: translateY(10px);
		}
		66% {
			-webkit-transform: translateY(-10px);
			transform: translateY(-10px);
		}
		100% {
			-webkit-transform: translateY(0);
			transform: translateY(0);
		}
	}
	@keyframes sync {
		33% {
			-webkit-transform: translateY(10px);
			transform: translateY(10px);
		}
		66% {
			-webkit-transform: translateY(-10px);
			transform: translateY(-10px);
		}
		100% {
			-webkit-transform: translateY(0);
			transform: translateY(0);
		}
	}
</style>