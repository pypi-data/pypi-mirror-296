from jasmine import RTModelTemplateForBinaryLightCurve as rtm2l
import numpy as np
import pandas as pd


def easy_plot_lightcurve(rtmodel_template_two_lenses_):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    magnification, time_interval = rtmodel_template_two_lenses_.rtmodel_magnification_using_vbb()
    ax.scatter(time_interval, magnification, s=0.8, alpha=0.3)
    plt.show(dpi=600)


def light_curve_genarator(template_path, output_folder):
    desired_interval = 5 / 60 / 24  # 0.00347222  # (5 minutes in days)

    einstein_time_tE = 20.  # days for the source to cross the Einstein radius.
    template_line = 2
    template_path = '/Users/sishitan/Documents/Scripts/RTModel_project/RTModel/RTModel/data/TemplateLibrary.txt'

    n_points = math.ceil((4 * einstein_time_tE) / desired_interval) + 1

    rtmodel_template_two_lenses = rtm2l(template_line=template_line, path_to_template=template_path, input_peak_t1=2,
                                        input_peak_t2=6)

    mag, times = rtmodel_template_two_lenses.rtmodel_magnification_using_vbb(n_points=n_points)

    lc = np.array([times, mag])

    print('cadence_is_ ' + str(abs(24 * 60 * (times[0] - times[1]))))
def all_rtmodel_template_generator(template_path, output_folder):
    '''
    SIS: I accidentally committed this part and this function is not ready yet.
    DO NOT USE IT
    '''
    lines = np.arange(2, 114)
    times_peak = np.arange(1, 402, 5)
    times_peak_2 = np.arange(1, 402, 2)
    base_times_peak_2 = np.arange(1, 402, 4)
    shuffled_peak_2 = np.random.shuffle(base_times_peak_2)
    times_peak_2 = base_times_peak_2.append(shuffled_peak_2)

    # intervals =
    for line in lines:
        rtmodel_template_two_lenses = rtm2l(template_line=line,
                                            path_to_template=template_path,
                                            input_peak_t1=300,
                                            input_peak_t2=302)
        magnification, times = rtmodel_template_two_lenses.rtmodel_magnification_using_vbb()
        binary_lens_signal_df = pd.DataFrame({'Magnification': magnification,
                                              'times': times})
        binary_lens_signal_df.to_csv(f'{output_folder}_rtmodel_{line}.csv')


if __name__ == '__main__':
    template_path = '/Users/stela/Documents/Scripts/RTModel_project/RTModel/RTModel/data/TemplateLibrary.txt'
    rtmodel_template_two_lenses = rtm2l(template_line=2,
                                        path_to_template=template_path,
                                        input_peak_t1=300,
                                        input_peak_t2=302)
    # easy_plot_lightcurve(rtmodel_template_two_lenses)

