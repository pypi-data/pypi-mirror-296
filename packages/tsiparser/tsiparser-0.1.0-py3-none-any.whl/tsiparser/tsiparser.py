import pandas as pnd


def tsiparser(args, logger): 
    
    
    logger.debug("Reading the preovided excel file (--inexceldb)...")
    exceldb = pnd.ExcelFile(args.inexceldb)
    sheet_names = exceldb.sheet_names

    # check all sheets are present: 
    for i in ['R', 'M', 'authors']: 
        if i not in sheet_names:
            logger.error(f"Sheet {i} is missing!")
            return 1
    
    return 0