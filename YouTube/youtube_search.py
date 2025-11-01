"""
YouTube Data API を使用した動画検索スクリプト
特定のキーワードに基づいて動画を検索し、タイトルとURLを表示します。
"""

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import config

def search_youtube_videos(keyword, max_results=10):
    """
    YouTube Data APIを使用して動画を検索する関数
    
    Args:
        keyword (str): 検索キーワード
        max_results (int): 取得する結果の最大数（デフォルト: 10）
    
    Returns:
        list: 動画情報のリスト（タイトルとURLを含む辞書のリスト）
    """
    try:
        # YouTube Data API v3を構築
        # APIキーを使用してサービスオブジェクトを作成
        youtube = build('youtube', 'v3', developerKey=config.YOUTUBE_API_KEY)
        
        # 検索リクエストを実行
        # q: 検索クエリ（キーワード）
        # part: 返されるリソースプロパティを指定（snippetは基本的な情報を含む）
        # type: 検索タイプ（video, channel, playlistなど）
        # maxResults: 返される結果の最大数
        # order: 結果の並び順（relevance: 関連度順, date: 日付順, rating: 評価順, viewCount: 再生回数順, title: タイトル順）
        request = youtube.search().list(
            q=keyword,
            part='snippet',
            type='video',
            maxResults=max_results,
            order='relevance'
        )
        
        # APIリクエストを実行してレスポンスを取得
        response = request.execute()
        
        # 検索結果を格納するリスト
        videos = []
        
        # レスポンスから動画情報を抽出
        for item in response.get('items', []):
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            # YouTube動画のURLを構築
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            videos.append({
                'title': title,
                'url': url
            })
        
        return videos
    
    except HttpError as e:
        print(f"APIリクエストでエラーが発生しました: {e}")
        return []
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        return []


def display_results(videos):
    """
    検索結果をコンソールに表示する関数
    
    Args:
        videos (list): 動画情報のリスト
    """
    if not videos:
        print("検索結果が見つかりませんでした。")
        return
    
    print(f"\n=== 検索結果 ({len(videos)}件) ===\n")
    
    for i, video in enumerate(videos, 1):
        print(f"{i}. {video['title']}")
        print(f"   URL: {video['url']}\n")


def main():
    """
    メイン処理
    """
    # 検索キーワードを入力（コマンドライン引数から取得することも可能）
    keyword = input("検索キーワードを入力してください: ")
    
    if not keyword:
        print("キーワードが入力されていません。")
        return
    
    # 取得する結果数を入力（オプション）
    try:
        max_results_input = input("取得する結果数（デフォルト: 10）: ")
        max_results = int(max_results_input) if max_results_input else 10
    except ValueError:
        print("無効な数値が入力されました。デフォルト値（10）を使用します。")
        max_results = 10
    
    print(f"\n「{keyword}」を検索中...\n")
    
    # 動画を検索
    videos = search_youtube_videos(keyword, max_results)
    
    # 結果を表示
    display_results(videos)


if __name__ == "__main__":
    main()

