# coding=utf-8
import cv2
import sys
import pyzbar.pyzbar as pyzbar
import requests
import json
# --------------------参数-----------------------------
result = {}         #解析结果

# ----------------------------------------------------

def decode(image):  # 解码
    barcodes = pyzbar.decode(image)
    for barcode in barcodes:
        # 提取并绘制图像中条形码的边界框
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        # 绘出图像上条形码的数据和条形码类型
        text = "Text:" + barcodeData
        text2 = "Type:" + barcodeType
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, text, (30, 30), font, 0.8, (0, 255, 0), 2)
        cv2.putText(image, text2, (30, 80), font, 0.8, (0, 255, 0), 2)
        if text:
            print(f'条形码为:{text}\n类型为:{text2}')
            inquiry(text[5:])





def camera():
    camera = cv2.VideoCapture('rtsp://admin:admin@192.168.5.47:8554/live')
    while True:
        # 读取当前帧
        ret, img = camera.read()
        decode(img)
        if result !={}:
            break
        img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
        cv2.imshow("camera", img)
        # 按q键退出程序
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()


def inquiry(code):
    appcode = 'f77362cc2baa41c08089a7a9bb1d3391'
    headers = {'Authorization':'APPCODE ' + appcode,
               'Content-Type':'application/json; charset=UTF-8'}


    host = 'https://jisutxmcx.market.alicloudapi.com'
    path = '/barcode2/query'
    querys = 'barcode=' + code
    url = host + path + '?' + querys

    res = requests.get(url,headers = headers)
    print(res.json()['msg'])
    if res.json()['result']:
        print('检测到结果！')

        for key,value in res.json()['result'].items():
            if value != '':
                # print(f'{key}:{value}')
                result[key] = value


def preserve(**kwargs):
    commodity = {}
    key = kwargs['name']
    commodity[key] = []
    commodity[key].append(kwargs['barcode'])

    with open('商品条码数据.json','r',encoding = 'utf-8')as file:
        old = json.load(file)
    with open('商品条码数据.json','w',encoding = 'utf-8')as file:
        old.update(commodity)
        json.dump(old,file,ensure_ascii=False)
        print('写入成功！')



if __name__ == '__main__':
    camera()
    print(result)
    preserve(**result)

