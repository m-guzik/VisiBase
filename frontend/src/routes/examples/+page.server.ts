import { instances } from '../sample_instances.js';

export function load() {
	return {
		samples: instances.map((instance) => ({
			name: instance.name,
			page: instance.page,
		}))
	};
}
