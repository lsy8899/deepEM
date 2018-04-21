class Train_Args():
    output_cnn_name             =       "data/19S.cnn"
    boxsize                     =       160
    dim_x                       =       1855
    dim_y                       =       1919
    name_length                 =       5
    name_prefix                 =       "image_"
    mic_path                    =       "data/19Sdata/mic/"
    positive1_box_path          =       "data/19Sdata/positive/"
    negative1_box_path          =       "data/19Sdata/negative/"
    positive1_mic_start_num     =       30001
    positive1_mic_end_num       =       30050
    negative1_mic_start_num     =       30001
    negative1_mic_end_num       =       30050
    do_train_again              =       0
    num_positive1               =       800
    num_negative1               =       800
    num_positive2               =       800
    num_negative2               =       800

    positive2_box_path          =       "data/19Sdata/sel_positive/"
    negative2_box_path          =       "data/19Sdata/sel_negative/"
    positive2_mic_start_num     =       30051
    positive2_mic_end_num       =       30090
    negative2_mic_start_num     =       30051
    negative2_mic_end_num       =       30100

    rotation_angel              =       90
    rotation_n                  =       4
    num_p_test                  =       150
    num_n_test                  =       150

    FL_feature_map              =       6
    FL_kernelsize               =       20

    SL_poolingsize              =       3

    TL_feature_map              =       12
    TL_kernelsize               =       10

    FOL_poolingsize             =       2

    FIL_feature_map             =       12
    FIL_kernelsize              =       4

    SIL_poolingsize             =       2

    alpha                       =       0.01
    batch_size                  =       50
    num_epochs                  =       20
    decay_rate                  =       0.96
    decay_step                  =       200
    sigma                       =       0.0001
    grad_step                   =       0
    keep_prob                   =       1.0


class Predict_Args():
    cnn_file                    =       "data/19S.cnn"
    data_path                   =       "data/19Sdata"
    boxsize                     =       160
    start_mic_num               =       30200
    end_mic_num                 =       30250
    dim_x                       =       1855
    dim_y                       =       1919
    scan_step                   =       20
    range1                      =       70
    range2                      =       40
    min_std                     =       22
    max_std                     =       34
    name_length                 =       5
    name_prefix                 =       "image_"
    rotation_angel              =       90
