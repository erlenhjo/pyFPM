# FPM imports
from pyFPM.NTNU_specific.simulate_images.cameraman import simulate_cameraman_2x
from pyFPM.recovery.algorithms.run_algorithm import recover, Method

# import plotting
from plotting.plot_simulation_results import plot_simulation_results


def main():
    method = Method.Fraunhofer_Epry_Gradient_Descent
    loops = 100

    setup_parameters, data_patch, imaging_system, illumination_pattern, applied_pupil\
        = simulate_cameraman_2x(noise_fraction=0, zernike_coefficients=[0,0,0,0,0.1])


    # define pupil
    pupil_guess = applied_pupil * 0 + 1

    algorithm_result = recover(
        method=method,
        data_patch=data_patch,
        imaging_system=imaging_system,
        illumination_pattern=illumination_pattern,
        pupil_guess=pupil_guess,
        loops=loops
    )

    plot_simulation_results(data_patch, illumination_pattern, imaging_system, algorithm_result)

    print(algorithm_result.convergence_index)


def profile_main():
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        main()
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename=r"profiling_data\simulate_and_recover_jitted_fftshifts.prof")

if __name__ == "__main__":
    #profile_main()
    main()