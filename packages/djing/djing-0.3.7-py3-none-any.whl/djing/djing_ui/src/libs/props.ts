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
};
