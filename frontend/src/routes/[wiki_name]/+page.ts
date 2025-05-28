import type { PageLoad } from './$types';

export const load: PageLoad = ({ params, url }) => {
  return {
    name: params.wiki_name,
    endpoint: url.searchParams.get('endpoint') ?? '',
    url: url.searchParams.get('url') ?? '',
    api: url.searchParams.get('api') ?? ''
  };
};
