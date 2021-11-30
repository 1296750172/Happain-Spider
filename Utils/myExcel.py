#coding=utf-8
import xlwt
import xlrd
import datetime

class Excel_write():
    def __init__(self,path):
        self.path=path
        self.ex=xlwt.Workbook()

        pass


    def add_sheet(self,name,data_list,col=-1):

        sheet_list=[]
        if type(name)==list:
            for i in name:
                sh=self.ex.add_sheet(i, cell_overwrite_ok=True)
                if col!=-1:
                    self.set_width(sh,len(data_list),col)
                self.write(sh,0,data_list)

                sheet_list.append(sh)

            return sheet_list
        else:
            sh = self.ex.add_sheet(name, cell_overwrite_ok=True)
            if col != -1:
                self.set_width(sh, len(data_list), col)
            self.writes(sh, 0, data_list)
            return  sh



    def write(self, sheet, hang, data, index):
        for i in zip(index, data):
            sheet.write(hang, i[0], i[1])


    def writes(self,sheet,hang,data):
        for i in range(0,len(data)):
            sheet.write(hang,i,data[i])


    def set_width(self,sh,long_num,width):
        for i in range(0,long_num):
            sh.col(i).width = 256 * width


    def save(self):
        self.ex.save(self.path)





class Excel_read():
    def __init__(self,path):
        self.ex=xlrd.open_workbook(path)

        pass

    def get_sheet_by_index(self,num):
        return self.ex.sheets()[num]

    def get_sheet_by_name(self,name):
        return self.ex.sheet_by_name(name)

    def get_all_sheet(self):
        return self.ex.sheets()

    def get_all_sheet_name(self):
        return self.ex.sheet_names()

    # 检查某个sheet是否导入完毕
    def check_sheet_is_load_by_name(self,name):
        return self.ex.sheet_loaded(name)
    def check_sheet_is_load_by_index(self,index):
        return self.ex.sheet_loaded(index)

    # 返回名字 列数 行数
    def get_name_ncols_nrows(self,sh):
        return [sh.name,sh.ncols,sh.nrows]


    # 获取某一列的数据
    def get_ncols_data(self,sh,num):
        return sh.col_values(num)

    # 返回某一行数据
    def get_nrows_data(self,sh,num):
        return sh.row_values(num)


    # 转换时间 (33656.0 转  #1990/2/22
    def format_date(self,data):
        date_value = xlrd.xldate_as_tuple(data, self.ex.datemode)
        date_tmp = datetime.date(*date_value[:3]).strftime('%Y/%m/%d')
        return date_tmp


    # 转换时间到时间

    def format_time(self, data):
        date_value = xlrd.xldate_as_tuple(data, self.ex.datemode)
        date_tmp = datetime.time(*date_value[3:]).strftime('%H:%M:%S')
        return date_tmp


if __name__ == '__main__':
    s=[['880501', '含H股'], ['880502', '含B股'], ['880503', '皖江区域'], ['880504', '长株潭'], ['880505', '稀缺资源'], ['880506', '5G概念'], ['880507', '国防军工'], ['880513', '海峡西岸'], ['880515', '通达信88'], ['880516', 'ST板块'], ['880519', '低碳经济'], ['880520', '智能电网'], ['880521', '黄金概念'], ['880522', '成渝特区'], ['880523', '黄河三角'], ['880524', '含可转债'], ['880525', '铁路基建'], ['880526', '长三角'], ['880527', '珠三角'], ['880528', '环渤海'], ['880529', '次新股'], ['880530', '三网融合'], ['880531', '武汉规划'], ['880533', '物联网'], ['880534', '锂电池'], ['880535', '稀土永磁'], ['880536', '多晶硅'], ['880537', '核电核能'], ['880540', '创投概念'], ['880542', '水利建设'], ['880544', '太阳能'], ['880545', '云计算'], ['880546', '卫星导航'], ['880547', '电子支付'], ['880548', '新三板'], ['880549', '可燃冰'], ['880550', '保障房'], ['880551', '涉矿概念'], ['880552', '金融改革'], ['880553', '页岩气'], ['880554', '东亚自贸'], ['880556', 'IP变现'], ['880557', '生物疫苗'], ['880558', '节能'], ['880560', '高端装备'], ['880563', '食品安全'], ['880564', '奢侈品'], ['880566', '图们江'], ['880567', '海南自贸'], ['880568', '生物质能'], ['880569', '3D打印'], ['880570', '海水淡化'], ['880571', '碳纤维'], ['880572', '新零售'], ['880574', '苹果概念'], ['880575', '地热能'], ['880577', '安防服务'], ['880578', '建筑节能'], ['880579', '生态农业'], ['880580', '智能交通'], ['880581', '空气治理'], ['880582', '风能'], ['880583', '充电桩'], ['880584', '石墨烯'], ['880585', '风沙治理'], ['880586', '土地流转'], ['880587', '聚氨酯'], ['880588', '绿色照明'], ['880589', '智能穿戴'], ['880590', '网络游戏'], ['880591', '上海自贸'], ['880592', '互联金融'], ['880593', '婴童概念'], ['880594', '一带一路'], ['880595', '民营银行'], ['880596', '体育概念'], ['880597', '养老概念'], ['880598', '博彩概念'], ['880599', '民营医院'], ['880600', '油气改革'], ['880701', '国资驰援'], ['880703', '科创概念'], ['880704', '工业大麻'], ['880705', '氢能源'], ['880706', '分散染料'], ['880707', '透明工厂'], ['880709', '人造肉'], ['880710', '种业'], ['880711', '操作系统'], ['880901', '信息安全'], ['880902', '特斯拉'], ['880903', '水域改革'], ['880904', '智能机器'], ['880905', '超导概念'], ['880906', '智能家居'], ['880907', '蓝宝石'], ['880908', '在线教育'], ['880909', '燃料电池'], ['880910', '草甘膦'], ['880911', '雄安新区'], ['880912', '电商概念'], ['880913', '基因概念'], ['880915', '职业教育'], ['880916', '国产软件'], ['880917', '央企改革'], ['880918', '全息概念'], ['880919', '粤港澳'], ['880920', '免疫治疗'], ['880921', '阿里概念'], ['880922', '钛金属'], ['880923', '赛马概念'], ['880925', '特钢'], ['880926', '固废处理'], ['880927', '抗癌'], ['880928', '抗流感'], ['880929', '维生素'], ['880930', '汽车电子'], ['880931', '装饰园林'], ['880932', '农村金融'], ['880933', '智能医疗'], ['880935', '智能电视'], ['880936', '猪肉'], ['880937', '网贷概念'], ['880938', '污水处理'], ['880939', '无人机'], ['880940', 'PPP模式'], ['880941', '跨境电商'], ['880942', '虚拟现实'], ['880943', '量子通信'], ['880944', '无人驾驶'], ['880945', 'OLED概念'], ['880946', '区块链'], ['880947', '债转股'], ['880948', '人工智能'], ['880949', '智慧城市'], ['880950', '军民融合'], ['880951', '新能源车'], ['880952', '芯片'], ['880953', '租购同权'], ['880954', '大数据'], ['880955', '乡村振兴'], ['880956', '腾讯概念'], ['880957', '工业互联'], ['880958', '独角兽'], ['880959', '知识产权'], ['880960', '仿制药'], ['880961', '小米概念'], ['880962', '百度概念'], ['880963', '华为概念'], ['880964', '特高压'], ['880511', '承诺注资'], ['880532', '整体上市'], ['880538', '参股金融'], ['880539', '股权激励'], ['880543', '外资背景'], ['880559', '要约收购'], ['880562', '高校背景'], ['880565', '送转潜力'], ['880573', '摘帽'], ['880576', '重组股'], ['880702', '壳资源'], ['880708', '台资背景'], ['880771', 'MSCI中盘'], ['880801', '基金重仓'], ['880802', 'QFII重仓'], ['880803', '券商重仓'], ['880804', '信托重仓'], ['880805', '保险重仓'], ['880806', '社保重仓'], ['880807', '高管增持'], ['880808', '高管减持'], ['880809', '基金独门'], ['880810', '陆股通买'], ['880811', '陆股通卖'], ['880812', '昨日连板'], ['880813', '重组预案'], ['880814', '拟增持'], ['880815', '拟减持'], ['880816', '密集调研'], ['880817', '商誉减值'], ['880821', '大盘股'], ['880823', '小盘股'], ['880824', '高市盈率'], ['880826', '低市盈率'], ['880827', '高市净率'], ['880829', '低市净率'], ['880833', '亏损股'], ['880834', '微利股'], ['880835', '绩优股'], ['880836', '配股股'], ['880837', '活跃股'], ['880842', '业绩预升'], ['880843', '业绩预降'], ['880844', '预计扭亏'], ['880845', '高股息股'], ['880846', '破净资产'], ['880847', '行业龙头'], ['880848', '被举牌'], ['880849', '股份回购'], ['880850', '定增预案'], ['880851', '已高送转'], ['880852', '参股新股'], ['880853', '中字头'], ['880854', '预高送转'], ['880856', '定增股'], ['880857', '证金持股'], ['880858', '国开持股'], ['880859', '员工持股'], ['880860', '扣非亏损'], ['880861', '连续亏损'], ['880863', '昨日涨停'], ['880864', '昨日振荡'], ['880865', '近期新高'], ['880866', '近期新低'], ['880867', '昨高换手'], ['880868', '高贝塔值'], ['880869', '股权转让'], ['880870', '两年新股'], ['880871', '股权分散'], ['880872', '最近复牌'], ['880873', '个人持股'], ['880874', '昨曾涨停'], ['880875', '中小银行'], ['880876', '户数增加'], ['880877', '户数减少'], ['880878', '百元股'], ['880879', '低价股'], ['880880', '上周强势'], ['880881', '上周弱势'], ['880882', '久不分红'], ['880883', 'MSCI成份'], ['880884', '近期异动'], ['880885', '次新开板'], ['880886', '昨日较强'], ['880887', '次新超跌'], ['880889', '不活跃股'], ['880890', '配股预案'], ['880891', '破发行价'], ['880892', '高质押股'], ['880893', '送转超跌'], ['880894', '养老金'], ['880895', '持续增长'], ['880896', '风险提示'], ['880897', '近期解禁'], ['880231', '西藏板块'], ['880214', '宁夏板块'], ['880203', '吉林板块'], ['880205', '辽宁板块'], ['880232', '内蒙板块'], ['880222', '江西板块'], ['880210', '广西板块'], ['880204', '甘肃板块'], ['880226', '江苏板块'], ['880219', '湖北板块'], ['880221', '湖南板块'], ['880202', '新疆板块'], ['880230', '海南板块'], ['880208', '陕西板块'], ['880216', '上海板块'], ['880218', '深圳板块'], ['880225', '重庆板块'], ['880211', '河北板块'], ['880220', '福建板块'], ['880213', '河南板块'], ['880212', '广东板块'], ['880224', '安徽板块'], ['880223', '四川板块'], ['880215', '山东板块'], ['880228', '浙江板块'], ['880227', '云南板块'], ['880209', '天津板块'], ['880207', '北京板块'], ['880201', '黑龙江'], ['880206', '青海板块'], ['880217', '山西板块'], ['880229', '贵州板块']]
    print(s)
    pass