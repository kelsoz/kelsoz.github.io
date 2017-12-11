# -*- coding: utf-8 -*-

import os,shutil
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )


GIF_THUMB = False

def get_project_info(project_dir):

    info_dic = {"thumb_name":"我是封面名","project_path_name":"2","title":"我是标题","subtitle":"Creative by kelso.z","tag":"我是tag","filter":"我是filter","content":"我是内容","date":"我是日期","tools":"我是工具","client":"我是客户"}
    info_dic["project_path_name"] = project_dir.split("/")[-1]
    for i in os.listdir(project_dir): # 遍历指定目录

        item = project_dir + "/"+ i
        if os.path.isfile(item) and os.path.splitext(item)[1] == '.txt': # 判断是否为.txt文件
            print "找到txt文件:",item
            f = open(item) # 打开文件
            for line in f: # 读入文件的每一行
                if line.startswith('title:'): # 根据每行开始内容获取数据
                    info_dic["title"] = line[6:]
                elif line.startswith("subtitle:"):
                    info_dic["subtitle"] = line[9:]
                elif line.startswith("tag:"):
                    info_dic["tag"] = line[4:]
                elif line.startswith("filter:"):
                    info_dic["filter"] = line[7:]
                elif line.startswith("date:"):
                    info_dic["date"] = line[5:]
                elif line.startswith("tools:"):
                    info_dic["tools"] = line[6:]
                elif line.startswith("client:"):
                    info_dic["client"] = line[7:]
                elif line.startswith("content:"):
                    info_dic["content"] = line[8:]
                else:
                    info_dic["content"] = info_dic["content"] + "<br>" + line
                    
            f.close() # 关闭文件
        elif os.path.isfile(item) and "thumb" in i:
            print "封面名:",i
            info_dic["thumb_name"] = i
    
    return info_dic

def get_project_img(project_dir):
    img_ex = [".jpg",".JPG",".jpeg",".JPEG",".png",".PNG",".gif"]
    img_list = []
    for item in os.listdir(project_dir): # 遍历指定目录
        item = project_dir + "/"+ item
        if os.path.isfile(item) and os.path.splitext(item)[1] in img_ex: # 判断是否为图像文件
            print item
            img_name = os.path.split(item)[1]
            if "thumb" in img_name:
                pass
            else:
                img_list.append(os.path.split(item)[1])
    
    return img_list




def main(project_path):
    info_dic = get_project_info(project_path)
    img_list = get_project_img(project_path)

    nowFilePath = os.getcwd()
    if "dribbble" in info_dic["tag"]:
        tmp_file = nowFilePath + "/single_project_dribbble_tp.html"
    else:
        tmp_file = nowFilePath + "/single_project_tp.html"
    f = open(tmp_file)
    html = f.read()



    # 更新标题与内容
    html = html.replace("@标题占位符",info_dic["title"]).replace("@副标占位符",info_dic["subtitle"]).replace("@内容占位符",info_dic["content"]).replace("@日期占位符",info_dic["date"]).replace("@工具占位符",info_dic["tools"]).replace("@客户占位符",info_dic["client"]).replace("@类别占位符",info_dic["tag"])

    # 插入图片
    for img in img_list:
        if "#" in img:
            img_html = "\t\t\t<img src=\"./%s\" alt=\"\" class=\"img-responsive\" />\n<!-- 图片图片占位符 -->"%img
        else:
            img_html = "\t\t\t<img src=\"./%s\" alt=\"\" class=\"img-responsive\" /><br>\n<!-- 图片图片占位符 -->"%img
        # print img_html
        html = html.replace("<!-- 图片图片占位符 -->",img_html)

    # 写入项目文件夹
    final_file = project_path + '/single-project.html'
    f2=file(final_file,"w+")
    f2.write(html)
    f2.close()
    f.close()
    return 1


def index_main(info_dic_list):
    nowFilePath = os.getcwd()
    tmp_file = nowFilePath + "/index_tp.html"

    f = open(tmp_file)
    html = f.read()

    for info_dic in info_dic_list:
        single_project_html = """<!-- single work -->
                        <div class="col-md-4 col-sm-6  %s">
                            <a href="./portflio/%s/single-project.html" class="portfolio_item" target="_blank">
                                <img src="./portflio/%s/%s" alt="image" class="img-responsive" />
                                <div class="portfolio_item_hover">
                                    <div class="portfolio-border clearfix">
                                        <div class="item_info">
                                            <span>%s</span>
                                            <em>%s</em>
                                        </div>
                                    </div>
                                </div>
                            </a>
                        </div>
                        <!-- end single work -->
                        <!-- @首页案例占位符 -->"""%(info_dic["filter"].strip(),info_dic["project_path_name"].strip(),info_dic["project_path_name"].strip(),info_dic["thumb_name"],info_dic["title"].strip(),info_dic["tag"].strip())
        html = html.replace("<!-- @首页案例占位符 -->",single_project_html)
        # global GIF_THUMB
        # print GIF_THUMB
        # if GIF_THUMB:
        #     html = html.replace("thumb.jpg","thumb.gif")
    # print html

    # 写入index
    final_file = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))  + '/index.html'
    f2=file(final_file,"w+")
    f2.write(html)
    f2.close()
    f.close()
    return 1


project_dir_list = []
main_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) 
main_path = os.path.join(main_path,"portflio")

# 取得所有作品文件夹路径
for item in os.listdir(main_path): # 遍历指定目录
    item = os.path.join(main_path,item)
    if os.path.isdir(item) : # 判断是否为目录
        project_dir_list.append(item)


# 为每个作品生成单个项目html
for project_path in project_dir_list:
    main(project_path)

# 生成首面html
info_dic_list = []
for project_path in project_dir_list:
    info_dic = get_project_info(project_path)
    info_dic_list.append(info_dic)

index_main(info_dic_list)


