import os

main_dir = os.path.dirname(os.getcwd())
os.makedirs(main_dir + '/collector/', exist_ok=True)
collector_dir = os.path.join(main_dir, 'collector/')

os.makedirs(collector_dir + '/rir/', exist_ok=True)
os.makedirs(main_dir + '/data/', exist_ok=True)
os.makedirs(main_dir + '/utils/', exist_ok=True)
os.makedirs(main_dir + '/communities/', exist_ok=True)

data_dir = os.path.join(main_dir, 'data/')
utils = os.path.join(main_dir, 'utils/')

com_dir = os.path.join(main_dir, 'communities/')
com_dict = os.path.join(com_dir, 'com_dict.txt')
com_text = os.path.join(com_dir, 'com_text.txt')
com_prepends = os.path.join(com_dir, 'prepends.txt')
com_no_export = os.path.join(com_dir, 'no_export.txt')
com_no_advertise = os.path.join(com_dir, 'no_advertise.txt')
com_blackhole = os.path.join(com_dir, 'blackhole.txt')
com_not_send = os.path.join(com_dir, 'not_send.txt')

com_ases = os.path.join(com_dir, 'ases.txt')
collected = os.path.join(com_dir, 'collected.txt')

os.makedirs(data_dir + '/ripe/', exist_ok=True)
os.makedirs(utils + '/ripe/', exist_ok=True)

os.makedirs(data_dir + '/afrinic/', exist_ok=True)
os.makedirs(utils + '/afrinic/', exist_ok=True)

os.makedirs(data_dir + '/apnic/', exist_ok=True)
os.makedirs(utils + '/apnic/', exist_ok=True)

os.makedirs(data_dir + '/arin/', exist_ok=True)
os.makedirs(utils + '/arin/', exist_ok=True)

os.makedirs(data_dir + '/lacnic/', exist_ok=True)
os.makedirs(utils + '/lacnic/', exist_ok=True)

ripe_dir = os.path.join(data_dir, 'ripe/')
ripe_utils = os.path.join(utils, 'ripe/')
ripe_log = os.path.join(ripe_utils, 'ripe_last.txt')
ripe_limit = os.path.join(ripe_utils, 'ripe_limit.txt')
ripe_list = os.path.join(ripe_utils, 'ripe_list.txt')

arin_dir = os.path.join(data_dir, 'arin/')
arin_utils = os.path.join(utils, 'arin/')
arin_log = os.path.join(arin_utils, 'arin_last.txt')
arin_limit = os.path.join(arin_utils, 'arin_limit.txt')
arin_list = os.path.join(arin_utils, 'arin_list.txt')

afrinic_dir = os.path.join(data_dir, 'afrinic/')
afrinic_utils = os.path.join(utils, 'afrinic/')
afrinic_log = os.path.join(afrinic_utils, 'afrinic_last.txt')
afrinic_limit = os.path.join(afrinic_utils, 'afrinic_limit.txt')
afrinic_list = os.path.join(afrinic_utils, 'afrinic_list.txt')

apnic_dir = os.path.join(data_dir, 'apnic/')
apnic_utils = os.path.join(utils, 'apnic/')
apnic_log = os.path.join(apnic_utils, 'apnic_last.txt')
apnic_limit = os.path.join(apnic_utils, 'apnic_limit.txt')
apnic_list = os.path.join(apnic_utils, 'apnic_list.txt')

lacnic_dir = os.path.join(data_dir, 'lacnic/')
lacnic_utils = os.path.join(utils, 'lacnic/')
lacnic_log = os.path.join(lacnic_utils, 'lacnic_last.txt')
lacnic_limit = os.path.join(lacnic_utils, 'lacnic_limit.txt')
lacnic_list = os.path.join(lacnic_utils, 'lacnic_list.txt')
