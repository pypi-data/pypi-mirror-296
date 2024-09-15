export type PageProps = {
  user_id: number,
  djing_config: {
    base_url: string,
    auth: {
      username_field: string,
    },
    resource_classes: {
      [key: string]: [
        {
          resource_key: string,
          resource_name: string,
          resource_plural_name: string,
        }
      ],
    },
  },
  djing_urls: {
    [key: string]: string,
  },
  user: {
    id: number,
    username: string,
    email: string,
    first_name?: string,
    last_name?: string,
  } | null,
};
