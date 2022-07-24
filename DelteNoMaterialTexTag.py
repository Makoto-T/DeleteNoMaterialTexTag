from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document


def main():

    # アンドゥを開始
    doc.StartUndo()
    
    # 最初のオブジェクトを取得する
    obj = doc.GetFirstObject()

    # オブジェクトが何もない場合終了
    if obj == None:
        return None

    # オブジェクトを while ループで処理
    while obj:
        
        # オブジェクトをタグを調べ，テクスチャタグでかつ
        # マテリアルが不明な場合は削除する
        Delete_Textag_No_Material(obj)
        
        # オブジェクトに階層がある場合はそのオブジェクトを取得
        obj = GetNextObject(obj)

    #アンドゥを終了
    doc.EndUndo()
    
    # エディタを更新する
    c4d.EventAdd()
    
    # 処理を終了
    return

# 階層をすべて調べる関数
def GetNextObject(obj):

    # 子オブジェクトを持っているかを調べる
    if obj.GetDown():
        # 子オブジェクトがあればobjに代入して返す
        obj = obj.GetDown()
        return obj

    # 次のオブジェクトがあるかどうかを調べる
    if obj.GetNext():
        # 次のオブジェクトがあればobjに代入して返す
        obj = obj.GetNext()
        return obj

    # いずれも無い場合は親階層に戻る
    while obj.GetUp():
        
        # objに親オブジェクト代入する
        obj = obj.GetUp()

        # 次のオブジェクトがあるかどうかを調べる
        if obj.GetNext():
            # objに次のオブジェクトを代入して返す
            obj = obj.GetNext()
            return obj

    # いずれも該当しない場合はfalseを返す
    return False


# マテリアルが適用されていないテクスチャタグを削除する関数
def Delete_Textag_No_Material(obj):

    # オブジェクトの最初のタグを代入する
    tag = obj.GetFirstTag()

    # タグをすべて調べる
    while tag:
        
        # テクスチャタグの場合
        if tag.GetType() == c4d.Ttexture:

            # テクスチャタグで，かつマテリアルが無い場合
            if not tag[c4d.TEXTURETAG_MATERIAL]:
                
                 # 削除する前にtempTag に次のタグを代入
                 tempTag = tag.GetNext()

                 # タグを削除するアンドゥを追加
                 doc.AddUndo(c4d.UNDOTYPE_DELETE, tag)

                 # テクスチャタグを削除する
                 tag.Remove()
            else:
                # tempTag に次のタグを代入
                tempTag = tag.GetNext()
        else:
            # テクスチャタグ以外の場合はtempTagに次のタグを代入
            tempTag = tag.GetNext()

        # tag に tempTagを代入してwhile処理を続ける

        tag = tempTag

    # 次のタグが無い場合は while を抜けて終了する
    return




if __name__=='__main__':
    main()