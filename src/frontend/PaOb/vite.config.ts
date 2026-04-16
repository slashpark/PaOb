import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		host: true, // Required for Docker to allow external connections
		proxy: {
		'/api': {
			target: process.env.VITE_API_URL || 'http://backend:8000', // Use backend service name in Docker
			changeOrigin: true,
			rewrite: (path) => path.replace(/^\/api/, '')
		}
		}
	}
});
