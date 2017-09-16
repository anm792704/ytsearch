import argparse

import httplib2

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


class YTChannel():
    def main():
        parser = argparse.ArgumentParser(description='Search youtube Videos by Title, Description')
        parser.add_argument("-t", "--title", help="pattern to search for in title", type=str)
        parser.add_argument("-d1", "--description1", help="pattern to search for in description", type=str)
        parser.add_argument("-d2", "--description2", help="additional pattern to search for in description", type=str)
        args = parser.parse_args()
        if args.title:
            print ("title to search for <" + args.title + ">")
        if args.description1:
            print ("description1 to search for <" + args.description1 + ">")
        if args.description2:
            print ("description2 to search for <" + args.description2 + ">")


        # The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
        # the OAuth 2.0 information for this application, including its client_id and
        # client_secret.
        CLIENT_SECRETS_FILE = "client_secret.json"

        # This OAuth 2.0 access scope allows for full read/write access to the
        # authenticated user's account and requires requests to use an SSL connection.
        #YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
        YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
        API_SERVICE_NAME = "youtube"
        API_VERSION = "v3"

        # This variable defines a message to display if the CLIENT_SECRETS_FILE is
        # missing.
        MISSING_CLIENT_SECRETS_MESSAGE = "WARNING: Please configure OAuth 2.0"

        # Authorize the request and store authorization credentials.
        def get_authenticated_service(args):
          flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
            message=MISSING_CLIENT_SECRETS_MESSAGE)

          #storage = Storage("%s-oauth2.json" % sys.argv[0])
          storage = Storage("youtube-api-snippets-oauth2.json")
          credentials = storage.get()

          if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage, args)

          # Trusted testers can download this discovery document from the developers page
          # and it should be in the same directory with the code.
          return build(API_SERVICE_NAME, API_VERSION,
              http=credentials.authorize(httplib2.Http()))

        service = get_authenticated_service(args)

        def remove_empty_kwargs(**kwargs):
            good_kwargs = {}
            if kwargs is not None:
                for key, value in kwargs.items():
                    if value:
                        good_kwargs[key] = value
            return good_kwargs

        def build_resource(properties):
            resource = {}
            for p in properties:
                # Given a key like "snippet.title", split into "snippet" and "title", where
                # "snippet" will be an object and "title" will be a property in that object.
                prop_array = p.split('.')
                ref = resource
                for pa in range(0, len(prop_array)):
                    is_array = False
                    key = prop_array[pa]
                    # Convert a name like "snippet.tags[]" to snippet.tags, but handle
                    # the value as an array.
                    if key[-2:] == '[]':
                        key = key[0:len(key) - 2:]
                        is_array = True
                    if pa == (len(prop_array) - 1):
                        # Leave properties without values out of inserted resource.
                        if properties[p]:
                            if is_array:
                                ref[key] = properties[p].split(',')
                            else:
                                ref[key] = properties[p]
                    elif key not in ref:
                        # For example, the property is "snippet.title", but the resource does
                        # not yet have a "snippet" object. Create the snippet object here.
                        # Setting "ref = ref[key]" means that in the next time through the
                        # "for pa in range ..." loop, we will be setting a property in the
                        # resource's "snippet" object.
                        ref[key] = {}
                        ref = ref[key]
                    else:
                        # For example, the property is "snippet.description", and the resource
                        # already has a "snippet" object.
                        ref = ref[key]
            return resource

        # Remove keyword arguments that are not set
        def remove_empty_kwargs(**kwargs):
            good_kwargs = {}
            if kwargs is not None:
                for key, value in kwargs.items():
                    if value:
                        good_kwargs[key] = value
            return good_kwargs

        # def print_results(results):
        #     print(results)
-
        def print_results(results, playlist_item_idx):
            print("----------- START ----------")
            print("Title: " + results['items'][playlist_item_idx]['snippet']['title'])
            print("Description: " + results['items'][playlist_item_idx]['snippet']['description'])
            print("URL: " + "https://youtube.com/watch?v=" + results['items'][playlist_item_idx]['snippet']['resourceId']['videoId'])
            print("----------- ENDE -----------")

        def playlist_items_list_by_playlist_id(service, **kwargs):
            kwargs = remove_empty_kwargs(**kwargs)  # See full sample for function
            results = service.playlistItems().list(
                **kwargs
            ).execute()

            #print_results(results)

            playlist_item_idx = 0
            while playlist_item_idx < len(results['items']):
                video_title_lower = results['items'][playlist_item_idx]['snippet']['title'].lower()
                video_description1_lower = results['items'][playlist_item_idx]['snippet']['description'].lower()
                video_description2_lower = results['items'][playlist_item_idx]['snippet']['description'].lower()

                if args.title is not None:
                    search_title_lower = args.title.lower()
                    if (search_title_lower in video_title_lower):
                        if args.description1 is not None:
                            search_description1_lower = args.description1.lower()
                            if (search_description1_lower in video_description1_lower):
                                if args.description2 is not None:
                                    search_description2_lower = args.description2.lower()
                                    if (search_description2_lower in video_description2_lower):
                                        print_results(results, playlist_item_idx)
                                else:
                                    print_results(results, playlist_item_idx)
                        else:
                            print_results(results, playlist_item_idx)
                else:
                    if args.description1 is not None:
                        search_description1_lower = args.description1.lower()
                        if (search_description1_lower in video_description1_lower):
                            if args.description2 is not None:
                                search_description2_lower = args.description2.lower()
                                if (search_description2_lower in video_description2_lower):
                                    print_results(results, playlist_item_idx)
                            else:
                                print_results(results, playlist_item_idx)
                playlist_item_idx = playlist_item_idx + 1

        def playlists_list_by_channel_id(service, **kwargs):
            kwargs = remove_empty_kwargs(**kwargs)  # See full sample for function
            results = service.playlists().list(
                **kwargs
            ).execute()

            # print_results(results)

            playlist_idx = 0
            while playlist_idx < len(results['items']):
                playlist_items_list_by_playlist_id(service,
                                                   part='snippet, contentDetails',
                                                   maxResults=25,
                                                   playlistId=results['items'][playlist_idx]['id'])
                playlist_idx = playlist_idx + 1

        playlists_list_by_channel_id(service,
                                     part='snippet,contentDetails',
                                     channelId='UCZ0DJ1UBmS1sEjDBr2OABAw',
                                     maxResults=50)

if __name__ == "__main__":
    YTChannel.main()