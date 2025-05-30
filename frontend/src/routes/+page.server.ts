import { instances } from './sample_instances.js';

export function load() {
	return {
		samples: instances.map((instance) => ({
			page: instance.page,
			name: instance.name,
		}))
	};
}
