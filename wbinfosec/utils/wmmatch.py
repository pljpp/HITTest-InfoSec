class WM:
    '''WM算法'''
    def __init__(self, mode):
        '''
        :param mode: 模式集合
        '''
        assert isinstance(mode, list)
        assert len(mode) > 0
        # 模式集合
        self.mode = mode
        # 最短字符串
        self.m = len(min(self.mode, key = len))
        # 分块
        self.b = min(2, self.m)
        # shift表
        self.shift = self.buildShift()
        # hash表和prefix表
        self.hashprefix = self.buildHashPrefix()
        # 模式串中未出现的子串的移动距离
        self.other = self.m - self.b + 1
        
    def buildShift(self):
        '''
        构建shift表, 索引为子串本身
        :return: shift表
        '''
        # 通过集合类型剔除重复的块
        block = set()
        # shift表
        shift = {}
        for mode in self.mode:
            # 考虑前m个字符的子串, 分隔为长度为b的块: 一共m-b+1块
            for i in range(self.m - self.b + 1):
                part = mode[i:i + self.b]
                block.add(part)
        # 初始化shift表
        for blk in block:
            value = self.m - self.b + 1
            shift.setdefault(blk, value)
        # 完善shift表
        for blk in shift:
            for mode in self.mode:
                if blk in mode[0:self.m]:
                    q = mode[0:self.m].index(blk)
                    shift[blk] = min(shift[blk], self.m - q - self.b)
        return shift
    
    def buildHashPrefix(self):
        '''
        构建hash表和prefix表, 索引为shift表的索引, 值为prefix表
        :return: 结合hash和prefix表构成的形如{后缀块, {前缀块, [模式串]}}的新表
        '''
        hashprefix = {}
        # hash表的索引
        for shift in self.shift:
            if self.shift.get(shift) == 0:
                hashprefix.setdefault(shift, {})
        for sufblk in hashprefix:
            # 未完善的prefix表, 其元素为元组类型, 元组的第一项将最终被完善为字典的索引
            mode_text = []
            for mode in self.mode:
                minmode = mode[0:self.m]
                if minmode.endswith(sufblk):
                    # 通过元组类型暂时存储前缀块与模式块本身的关系
                    mode_tuple = (minmode, mode)
                    mode_text.append(mode_tuple)
                    # 初始化prefix表中的模式串项为空列表, 防止原模式串中存在最小子串的前缀块和后缀块都相等的情况
                    hashprefix[sufblk][minmode[0:self.b]] = []
            # 完善prefix表, 形式为{前缀块, [模式串]}
            for preblk in hashprefix[sufblk]:
                for formode in mode_text:
                    # 元组的第1项完善为索引, 第2项为模式串本身
                    if formode[0].startswith(preblk):
                        hashprefix[sufblk][preblk].append(formode[1])
        return hashprefix
    
    def search(self, text):
        '''
        利用WM算法匹配字符串, 返回匹配结果
        :param text: 文本
        :return: 形如{mode, [(start, end)]}的字典, 索引为模式串, 元素为出现的起始位置和结束位置的列表
        '''
        # 匹配结果
        result = {}
        for mode in self.mode:
            result[mode] = []
        # 起始匹配位置
        site = self.m - self.b
        # 匹配
        while site <= len(text) - self.b:
            nowsuf = text[site:site + self.b]
            # 输出每次比较的子串: print(nowsuf)
            if nowsuf in self.shift:
                # 存在匹配, 查找hash表
                if self.shift[nowsuf] == 0:
                    if nowsuf in self.hashprefix:
                        # 原文中对应的模式前缀块的字符子串
                        nowpre = text[site - self.m + 2:site - self.m + self.b + 2]
                        # 查找prefix表
                        if nowpre in self.hashprefix[nowsuf]:
                            # 获得模式串列表
                            mode_list = self.hashprefix[nowsuf][nowpre]
                            for mode in mode_list:
                                # 待匹配的字符串
                                needmate = text[site - self.m + 2:site - self.m + 2 + len(mode)]
                                if mode == needmate:
                                    position = (site - self.m + 2, site - self.m + 2 + len(mode))
                                    result[mode].append(position)
                    else:
                        assert False, 'hash表构建错误'
                step = self.shift[nowsuf]
            else:
                # shift表中无索引则移动m-b+1格
                step = self.other
            # 匹配成功则前移1步
            if step == 0:
                step = 1
            # 更新待匹配子串
            site = site + step
        return result

class DHSWM(WM):
    '''
    新增slip表优化WM算法
    当shift表中移动值为0时, 将查找模式串, slip表用于存储进行匹配操作后匹配窗口可滑动的距离
    '''
    def __init__(self, mode):
        # 调用父类获得其shift表和hashprefix表
        WM.__init__(self, mode)
        # slip表
        self.slip = self.buildSlip()
    
    def buildSlip(self):
        '''
        构建slip表, 存储匹配子串块(并非整个模式串)成功后窗口可以滑动的最大距离
        :return: slip表
        '''    
        slip = {}
        # 模式串的最短子串
        minmode = set()
        for mode in self.mode:
            minmode.add(mode[0:self.m])
        for shift in self.shift:
            # 初始化所有的slip值为m-b+1
            if self.shift[shift] == 0:
                slip[shift] = self.other
                # 若shift出现在某个模式子串中的最后位置(结束位置除外)是q, 则取slip[shift]=m-q
                q = -1
                for mode in minmode:
                    find = mode.rfind(shift)
                    # 寻找除结束位置外的最大位置
                    if find > q and find != self.m - self.b:
                        q = find
                if q != -1:
                    slip[shift] = self.m - q
        return slip
    
    def search(self, text):
        '''
        重写WM算法中的search方法, 返回匹配结果
        :param text: 文本
        :return: 形如{mode, [(start, end)]}的字典, 索引为模式串, 元素为出现的起始位置和结束位置的列表
        '''
        # 匹配结果
        result = {}
        for mode in self.mode:
            result[mode] = []
        # 起始匹配位置
        site = self.m - self.b
        # 匹配
        while site <= len(text) - self.b:
            nowsuf = text[site:site + self.b]
            # 输出每次比较的子串: print(nowsuf)
            if nowsuf in self.shift:
                # 匹配窗口滑动距离
                step = self.shift[nowsuf]
                # 存在匹配, 查找hash表
                if self.shift[nowsuf] == 0:
                    # 子串块匹配成功, 匹配窗口滑动slip[nowsuf]距离
                    if nowsuf in self.slip:
                        step = self.slip[nowsuf]
                    else:
                        assert False, 'slip表构建错误'
                    if nowsuf in self.hashprefix:
                        # 原文中对应的模式前缀块的字符子串
                        nowpre = text[site - self.m + 2:site - self.m + self.b + 2]
                        # 查找prefix表
                        if nowpre in self.hashprefix[nowsuf]:
                            # 获得模式串列表
                            mode_list = self.hashprefix[nowsuf][nowpre]
                            for mode in mode_list:
                                # 待匹配的字符串
                                needmate = text[site - self.m + 2:site - self.m + 2 + len(mode)]
                                if mode == needmate:
                                    position = (site - self.m + 2, site - self.m + 2 + len(mode))
                                    result[mode].append(position)
                    else:
                        assert False, 'hash表构建错误'
            else:
                # shift表中无索引则移动m-b+1格
                step = self.other
            # 匹配成功则前移1步
            if step == 0:
                step = 1
            # 更新待匹配子串
            site = site + step
        return result

if __name__ == '__main__':
    # mode = ['the', 'she', 'che', 'this', 'think', 'third', 'hers']
    # text = 'she is thinking how to be thinner'
    mode = ['still', 'trill', 'study', 'basic', 'stability']
    text = 'this chapter will introduce the basic concepts'
    wm = DHSWM(mode)
    print(wm.shift)
    print(wm.hashprefix)
    print(wm.search(text))
