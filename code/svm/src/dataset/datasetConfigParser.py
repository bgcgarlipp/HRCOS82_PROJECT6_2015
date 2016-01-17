"""


"""
import ConfigParser as cp
from string import upper

def fill_it(parser, name, left_side):

    if left_side:
        fstr = '{0}_{1}'
    else:
        fstr = '{1}_{0}'

    config = {}
    for opt in parser.options(name):
        val = parser.get(name,opt)
        if upper(opt) == 'TOOL':
            try:
                with open(val):
                    pass
            except:
                val += '.exe'
                with open(val):
                    pass
        config[fstr.format(upper(opt), name)] = val

    return config

def parse_python_config(configFile):
    config={}
    execfile(configFile, config)
    return config

def parse_ini_config(configFile):
    config={}
    parser=cp.ConfigParser()
    parser.read(configFile)

#     classes=[]
#     for opt in parser.options('AUCLASSES'):
#         classes.append(opt)
#     config['AUCLASSES']=classes

    size={}
    for opt in parser.options('SIZE'):
        size[opt]=parser.get('SIZE',opt)
    config['SIZE']=size

    config.update(fill_it(parser, 'RECOG', False))
    config.update(fill_it(parser, 'TRAINING', False))
    config.update(fill_it(parser, 'VALIDATION', False))
    config.update(fill_it(parser, 'FOLDER', True))
    config.update(fill_it(parser, 'SUFFIX', True))

    config.update(fill_it(parser, 'FACECROP', False))
    config.update(fill_it(parser, 'GABOR', False))
    config.update(fill_it(parser, 'TRAIN', False))
    config.update(fill_it(parser, 'DETECTION', False))
    config.update(fill_it(parser, 'GUI', False))

    # Class lists incorperate the idea of AU and emotion
    clslist=[]
    
#     print "TYPE: {}".format(config["RECOG_TYPE"])
#     print "CLASSES: {}".format(config["RECOG_CLASS"])
#     print "DATABASE: {}".format(config["RECOG_DATABASE"])

    csvList = [int(x) for x in config["RECOG_CLASS"].replace(" ", "").split(',')]
    config['SEARCH_LIST'] = csvList
    
    if (config["RECOG_TYPE"].upper() == "EMOTION"):
        emolist = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"]
        config['EMOLIST']=emolist
        
        clslist.append("neutral");
        for (index, emo) in enumerate(emolist, start=0):
            if index in csvList:
                clslist.append(emo);
    else:
        for au in csvList:
            clslist.append( "AU{}".format(au) )
            
    config['CLSLIST']=clslist
    return config
