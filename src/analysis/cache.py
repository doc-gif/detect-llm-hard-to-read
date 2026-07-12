import matplotlib
import shutil
from pathlib import Path

# キャッシュディレクトリのパスを表示して削除
cache_dir = Path(matplotlib.get_cachedir())
print(f"キャッシュディレクトリ: {cache_dir}")

# キャッシュファイルを削除
if cache_dir.exists():
    shutil.rmtree(cache_dir)
    print("キャッシュを削除しました。次にPythonを再起動した際に再生成されます。")
else:
    print("キャッシュディレクトリが見つかりません。")