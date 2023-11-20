# kernel_AHC

このライブラリは、カーネル関数を使用した階層的クラスタリングとなっています。
使用する際には、zipをダウンロードしてください。
ライブラリをインストールする際は、zipファイルを解凍し、コマンドプロンプトやターミナルなどからpipを使用してインストールしてください。
setup.pyがあるディレクターをカレントディレクトリとし、「pip install .」と入力するとインストールできます。
アンインストールする場合には、「pip uninstall kernel_AHC」と入力してください。

使用する際には、kernel_AHCをimportし、使用したい手法のインスタンスを生成してください。
インスタンスの生成については以下のように行います。

```
obj = kernel_AHC.HC_single_linkage(input_data = dsim_list)
```

こちらのコードは最短距離法を用いる際のコードであり、そのほかの手法については「HC_single_linkage」を以下のものにしてください。（medoidと書かれているものは、クラスタの重心にmedoidを使用しているものです）

最短距離法：HC_single_linkage
最長距離法：HC_complete_linkage
群間平均法：HC_average_linkage_between
群内平均法：HC_average_linkage_within
重心法：HC_centroid
重心法(medoid)：HC_centroid_medoid
Ward法：HC_ward
Ward法(medoid)：HC_ward_medoid

dsim_listは非類似度行列を示しています。
非類似度行列については、距離行列を使用することも可能ですが、kernel_HC_dsimを使用することも可能です。
kernel_HC_dsimは、カーネル関数によって得られたカーネル行列を基に、写像空間上での距離行列を取得するものであり、引数にカーネル行列をndarrayの形式で与えてください。
以下は使用例です。（kernel_listがカーネル行列をndarrayの形式で表現したものです）

```
dsim_list = kernel_AHC.kernel_HC_dsim(kernel_list)
```

解析の実行、ラベルの表示、は以下のコードによって行います。

```
obj.fit()
obj.get_label_list(3)
obj.create_dendrogram()
```

get_label_list()は、引数の数にクラスタ分割を行い、結果のラベルを戻り値とします。
create_dendrogram()は、樹形図を作成し、現在のカレントディレクトリに画像ファイルを保存します。
