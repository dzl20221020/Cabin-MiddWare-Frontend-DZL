import cv2
import numpy as np
import os

def main():
    # 打开文件读取图像文件
    filename = "calibdata.txt"
    fin = open(filename, 'r')
    # 打开文件保存标定结果
    fout = open("caliberation_result.txt", 'w')

    # 读取每一幅图像，提取角点并进行亚像素精确化
    print("开始提取角点………………")
    image_count = 0  # 图像数量
    image_points_seq = []  # 保存检测到的所有角点

    while True:
        filename = fin.readline().strip()
        if not filename:  # 文件读取完毕
            break

        image_count += 1
        print(f"image_count = {image_count}")
        print(f"Trying to load image: {filename}")

        if not os.path.isfile(filename):
            print(f"File {filename} does not exist.")
            continue

        imageInput = cv2.imread(filename)
        if imageInput is None:
            print(f"Failed to load image {filename}")
            continue

        if image_count == 1:  # 读入第一张图片时获取图像宽高信息
            image_size = (imageInput.shape[1], imageInput.shape[0])  # 图像的宽高
            print(f"image_size.width = {image_size[0]}")
            print(f"image_size.height = {image_size[1]}")

        # 提取角点
        ret, corners = cv2.findChessboardCorners(imageInput, (4, 5), None)
        if not ret:  # 找不到角点
            print("can not find chessboard corners!")
            exit(1)

        # 亚像素精确化
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
        cv2.cornerSubPix(cv2.cvtColor(imageInput, cv2.COLOR_BGR2GRAY), corners, (5, 5), (-1, -1), criteria)
        image_points_seq.append(corners.reshape(-1, 2))  # 保存亚像素角点

        # 在图像上显示角点位置
        cv2.drawChessboardCorners(imageInput, (4, 5), corners, ret)
        cv2.imshow("Camera Calibration", imageInput)
        cv2.waitKey(500)  # 暂停0.5秒

    fin.close()
    cv2.destroyAllWindows()

    total = len(image_points_seq)
    print(f"total = {total}")

    CornerNum = 4 * 5  # 每张图片上总的角点数
    for ii in range(total * CornerNum):
        if ii % CornerNum == 0:  # 每24个角点换行输出
            i = ii // CornerNum
            j = i + 1
            print(f"--> 第 {j} 图片的数据 --> : ")

        # 打印角点坐标
        point = image_points_seq[ii // CornerNum][ii % CornerNum]
        if ii % 3 == 0:
            print()
        print(f"({point[0]:.2f}, {point[1]:.2f})", end=" ")

    print("角点提取完成！")

    # 摄像机标定
    print("开始标定………………")
    # 棋盘三维信息
    square_size = 10  # 实际测量得到的标定板上每个棋盘格的大小
    object_points = []  # 保存标定板上角点的三维坐标

    # 初始化标定板上角点的三维坐标
    for i in range(5):
        for j in range(4):
            object_points.append([j * square_size, i * square_size, 0])

    object_points = np.array(object_points, dtype=np.float32)  # 转换为numpy数组
    object_points_seq = [object_points] * total  # 生成所有图像的三维点列表

    # 将 image_points_seq 转换为 numpy 数组
    image_points_seq = [np.array(pts, dtype=np.float32) for pts in image_points_seq]

    # 开始标定
    ret, cameraMatrix, distCoeffs, rvecsMat, tvecsMat = cv2.calibrateCamera(
        object_points_seq, image_points_seq, image_size, None, None)
    print("标定完成！")

    # 对标定结果进行评价
    print("开始评价标定结果………………")
    total_err = 0.0  # 所有图像的平均误差的总和
    err = 0.0  # 每幅图像的平均误差

    print("\t每幅图像的标定误差：")
    fout.write("每幅图像的标定误差：\n")
    for i in range(len(image_points_seq)):
        # 重新计算投影点
        img_points, _ = cv2.projectPoints(object_points_seq[i], rvecsMat[i], tvecsMat[i], cameraMatrix, distCoeffs)
        img_points = img_points.reshape(-1, 2)  # 将 img_points 转换为 2D 点

        # 计算误差
        err = cv2.norm(image_points_seq[i], img_points, cv2.NORM_L2) / len(img_points)
        total_err += err

        print(f"第 {i + 1} 幅图像的平均误差：{err} 像素")
        fout.write(f"第 {i + 1} 幅图像的平均误差：{err} 像素\n")

    print(f"总体平均误差：{total_err / len(image_points_seq)} 像素")
    fout.write(f"总体平均误差：{total_err / len(image_points_seq)} 像素\n\n")
    print("评价完成！")

    # 保存定标结果
    print("开始保存定标结果………………")
    fout.write("相机内参数矩阵：\n")
    fout.write(f"{cameraMatrix}\n\n")
    fout.write("畸变系数：\n")
    fout.write(f"{distCoeffs}\n\n\n")

    for i in range(len(image_points_seq)):
        fout.write(f"第 {i + 1} 幅图像的旋转向量：\n")
        fout.write(f"{rvecsMat[i]}\n")

        R = np.zeros((3, 3), dtype=np.float32)
        cv2.Rodrigues(rvecsMat[i], R)
        fout.write(f"第 {i + 1} 幅图像的旋转矩阵：\n")
        fout.write(f"{R}\n")

        fout.write(f"第 {i + 1} 幅图像的平移向量：\n")
        fout.write(f"{tvecsMat[i]}\n\n")

    print("完成保存")
    fout.close()

    # 显示定标结果
    print("保存矫正图像")
    mapx, mapy = cv2.initUndistortRectifyMap(cameraMatrix, distCoeffs, None, cameraMatrix, image_size, cv2.CV_32FC1)
    for i in range(len(image_points_seq)):
        print(f"Frame #{i + 1}...")
        filename = f"E:\\doing\\touchscreen-display\\data\\data\\{i + 1}.jpg"
        imageSource = cv2.imread(filename)
        if imageSource is None:
            print(f"Failed to load image {filename}")
            continue
        newimage = cv2.remap(imageSource, mapx, mapy, cv2.INTER_LINEAR)
        output_filename = f"E:\\doing\\touchscreen-display\\data\\data\\{i + 1}_d.jpg"
        cv2.imwrite(output_filename, newimage)
        print(f"Saved corrected image as {output_filename}")

    print("保存结束")

if __name__ == "__main__":
    main()
