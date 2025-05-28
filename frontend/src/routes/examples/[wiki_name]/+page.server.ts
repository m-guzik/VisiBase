import { error } from '@sveltejs/kit';
import { instances } from '../../sample_instances.js';

export function load({ params }) {
    const instance = instances.find((instance) => instance.page === params.wiki_name);

    if(!instance) error(404);

    return { instance };
}
