from service.paradigmservice import ParadigmService

if __name__ == "__main__":
    paradigmService = ParadigmService()

    paradigms = paradigmService.getAllParadigm()

    # 解析数据
    for paradigm in paradigms:
        print(paradigm)
