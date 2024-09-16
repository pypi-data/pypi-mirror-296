import numpy as np


class NonlinearFeatures:
    """
    A class for computing nonlinear (geometric) features from physiological signals (ECG, PPG, EEG).

    Attributes
    ----------
    signal : np.array
        The physiological signal (e.g., ECG, PPG, EEG).
    fs : int
        The sampling frequency of the signal in Hz. Default is 1000 Hz.

    Methods
    -------
    compute_sample_entropy(m=2, r=0.2)
        Computes the sample entropy of the signal, measuring its complexity.
    compute_approximate_entropy(m=2, r=0.2)
        Computes the approximate entropy of the signal, quantifying its unpredictability.
    compute_fractal_dimension(kmax=10)
        Computes the fractal dimension of the signal using Higuchi's method.
    compute_lyapunov_exponent()
        Computes the largest Lyapunov exponent, indicating the presence of chaos in the signal.
    compute_dfa(order=1)
        Computes the detrended fluctuation analysis (DFA) for assessing fractal scaling.
    compute_poincare_features()
        Computes Poincaré plot features (SD1 and SD2) to assess short- and long-term HRV variability.
    compute_recurrence_features(threshold=0.2)
        Computes features from the recurrence plot, including recurrence rate, determinism, and laminarity.
    """

    def __init__(self, signal, fs=1000):
        """
        Initializes the NonlinearFeatures object.

        Args:
            signal (np.array): The physiological signal.
            fs (int): The sampling frequency of the signal in Hz. Default is 1000 Hz.
        """
        self.signal = np.array(signal)
        self.fs = fs  # Sampling frequency

    def compute_sample_entropy(self, m=2, r=0.2):
        """
        Computes the sample entropy of the signal. Sample entropy is a measure of signal complexity,
        specifically used for detecting the regularity and unpredictability of fluctuations in a signal.

        Args:
            m (int): Embedding dimension (default is 2).
            r (float): Tolerance (default is 0.2).

        Returns:
            float: The computed sample entropy of the signal.

        Example:
            >>> ecg_signal = [...]  # Sample ECG signal
            >>> nf = NonlinearFeatures(ecg_signal)
            >>> sample_entropy = nf.compute_sample_entropy()
            >>> print(f"Sample Entropy: {sample_entropy}")
        """
        if np.all(self.signal == 0) or np.std(self.signal) == 0:
            return 0  # Return 0 for constant or zero signals
        if len(self.signal) <= m:
            return 0  # Return 0 for signals too short for meaningful entropy

        def _phi(m):
            """
            Computes the _phi function for sample entropy calculation.
            Args:
                m (int): Embedding dimension.
            Returns:
                float: The computed _phi value.
            """
            N = len(self.signal)
            x = np.array([self.signal[i : i + m] for i in range(N - m + 1)])
            C = np.sum(
                np.sum(np.abs(x[i] - x[j]) < r)
                for i in range(len(x))
                for j in range(i + 1, len(x))
            )
            return C / (len(x) ** 2 - len(x))

        phi_m = _phi(m)
        phi_m1 = _phi(m + 1)

        if phi_m == 0 or phi_m1 == 0:
            return 0  # Avoid log of zero
        return -np.log(phi_m1 / phi_m)

    def compute_approximate_entropy(self, m=2, r=0.2):
        """
        Computes the approximate entropy of the signal. Approximate entropy quantifies the
        unpredictability and regularity of signal patterns.

        Args:
            m (int): Embedding dimension (default is 2).
            r (float): Tolerance (default is 0.2).

        Returns:
            float: The computed approximate entropy of the signal.

        Example:
            >>> ppg_signal = [...]  # Sample PPG signal
            >>> nf = NonlinearFeatures(ppg_signal)
            >>> approx_entropy = nf.compute_approximate_entropy()
            >>> print(f"Approximate Entropy: {approx_entropy}")
        """
        if np.all(self.signal == 0) or np.std(self.signal) == 0:
            return 0  # Return 0 for constant or zero signals
        if len(self.signal) <= m:
            return 0  # Return 0 for signals too short for meaningful entropy

        def _phi(m):
            x = np.array(
                [self.signal[i : i + m] for i in range(len(self.signal) - m + 1)]
            )
            C = np.sum(
                [
                    np.max(np.abs(x[i] - x[j])) < r
                    for i in range(len(x))
                    for j in range(len(x))
                    if i != j
                ]
            )
            return C / (len(self.signal) - m + 1)

        return _phi(m) - _phi(m + 1)

    def compute_fractal_dimension(self, kmax=10):
        """
        Computes the fractal dimension of the signal using Higuchi's method. Fractal dimension
        is a measure of complexity, reflecting how the signal fills space as its scale changes.

        Returns:
            float: The fractal dimension of the signal.

        Example:
            >>> eeg_signal = [...]  # Sample EEG signal
            >>> nf = NonlinearFeatures(eeg_signal)
            >>> fractal_dimension = nf.compute_fractal_dimension()
            >>> print(f"Fractal Dimension: {fractal_dimension}")
        """

        if len(self.signal) < kmax:
            return 0  # Return 0 for signals too short for the given kmax

        def _higuchi_fd(signal, kmax):
            Lmk = np.zeros((kmax, kmax))
            N = len(signal)
            for k in range(1, kmax + 1):
                for m in range(0, k):
                    Lm = 0
                    for i in range(1, int((N - m) / k)):
                        Lm += abs(signal[m + i * k] - signal[m + (i - 1) * k])
                    if int((N - m) / k) == 0:
                        return 0
                    Lmk[m, k - 1] = Lm * (N - 1) / ((int((N - m) / k) * k * k))

            Lk = np.sum(Lmk, axis=0) / kmax
            log_range = np.log(np.arange(1, kmax + 1))
            if np.any(Lk == 0):
                return 0  # Return 0 to avoid division by zero in polyfit
            return -np.polyfit(log_range, np.log(Lk), 1)[0]

        return _higuchi_fd(self.signal, kmax)

    def compute_lyapunov_exponent(self):
        """
        Computes the largest Lyapunov exponent (LLE) of the signal. LLE measures the rate at
        which nearby trajectories in phase space diverge, indicating chaotic behavior in the signal.

        Returns:
            float: The largest Lyapunov exponent of the signal.

        Example:
            >>> ecg_signal = [...]  # Sample ECG signal
            >>> nf = NonlinearFeatures(ecg_signal)
            >>> lyapunov_exponent = nf.compute_lyapunov_exponent()
            >>> print(f"Largest Lyapunov Exponent: {lyapunov_exponent}")
        """
        N = len(self.signal)
        if N < 3:
            return 0  # Not enough data for meaningful computation

        epsilon = np.std(self.signal) * 0.1
        max_t = min(
            int(N / 10), N - 3
        )  # Ensure max_t is not larger than the length of the phase space

        def _distance(x, y):
            return np.sqrt(np.sum((x - y) ** 2))

        def _lyapunov(time_delay, dim, max_t):
            if max_t <= 1:
                return 0  # Prevent division errors with too short signals
            phase_space = np.array([self.signal[i::time_delay] for i in range(dim)]).T

            divergences = []
            for i in range(len(phase_space) - max_t - 1):
                d0 = _distance(phase_space[i], phase_space[i + 1])
                d1 = _distance(phase_space[i + max_t], phase_space[i + max_t + 1])
                if d0 > epsilon and d1 > epsilon:
                    divergences.append(np.log(d1 / d0))

            if len(divergences) == 0:
                return 0  # Return 0 if no valid divergences were found
            return np.mean(divergences)

        return _lyapunov(time_delay=5, dim=2, max_t=max_t)

    def compute_dfa(self, order=1):
        """
        Computes the Detrended Fluctuation Analysis (DFA) of the signal. DFA is used to assess
        the fractal scaling properties of time-series data, especially in physiological signals.

        Args:
            order (int): The order of the polynomial fit for detrending. Default is 1 (linear detrending).

        Returns:
            float: The DFA scaling exponent (α).

        Example:
            >>> ecg_signal = [...]  # Sample ECG signal
            >>> nf = NonlinearFeatures(ecg_signal)
            >>> dfa = nf.compute_dfa(order=1)
            >>> print(f"DFA Scaling Exponent: {dfa}")
        """
        N = len(self.signal)
        if N < 4:
            return 0  # Not enough data for DFA computation

        def _integrated_signal(signal):
            return np.cumsum(signal - np.mean(signal))

        def _detrended_fluctuation(integrated_signal, n, order):
            segment_length = len(integrated_signal) // n
            fluctuations = np.zeros(n)
            for i in range(n):
                segment = integrated_signal[
                    i * segment_length : (i + 1) * segment_length
                ]
                x = np.arange(segment_length)
                poly = np.polyfit(x, segment, order)
                trend = np.polyval(poly, x)
                fluctuations[i] = np.sqrt(np.mean((segment - trend) ** 2))
            return fluctuations

        integrated_signal = _integrated_signal(self.signal)
        fluctuation_sizes = []
        scales = np.logspace(1, np.log10(N // 2), 50).astype(int)
        for scale in scales:
            fluctuation_sizes.append(
                np.mean(_detrended_fluctuation(integrated_signal, scale, order))
            )

        log_fluctuation_sizes = np.log(fluctuation_sizes)
        log_scales = np.log(scales)
        dfa_alpha = np.polyfit(log_scales, log_fluctuation_sizes, 1)[0]
        return dfa_alpha

    def compute_poincare_features(self, nn_intervals):
        """
        Computes the SD1 and SD2 features from the Poincaré plot of the NN intervals. SD1 reflects
        short-term HRV, while SD2 reflects long-term HRV.

        Returns:
            tuple: SD1 (short-term HRV), SD2 (long-term HRV).

        Example:
            >>> nf = NonlinearFeatures(signal)
            >>> nn_intervals = [800, 810, 790, 805, 795]
            >>> sd1, sd2 = nf.compute_poincare_features(nn_intervals=nn_intervals)
            >>> print(f"SD1: {sd1}, SD2: {sd2}")
        """
        diff_nn_intervals = np.diff(nn_intervals)
        sd1 = np.sqrt(np.var(diff_nn_intervals) / 2)
        sd2 = np.sqrt(2 * np.var(nn_intervals) - sd1**2)
        return sd1, sd2

    def compute_recurrence_features(self, threshold=0.2):
        """
        Computes features from the recurrence plot, including recurrence rate, determinism,
        and laminarity. These features provide insights into the recurrence of signal dynamics.

        Args:
            threshold (float): The threshold to define recurrences. Default is 0.2.

        Returns:
            dict: A dictionary containing recurrence rate, determinism, and laminarity.

        Example:
            >>> ecg_signal = [...]  # Sample ECG signal
            >>> nf = NonlinearFeatures(ecg_signal)
            >>> rqa_features = nf.compute_recurrence_features(threshold=0.2)
            >>> print(rqa_features)
        """
        N = len(self.signal)
        phase_space = np.array([self.signal[i::2] for i in range(2)]).T
        rec_matrix = (
            np.sqrt(
                np.sum(
                    (phase_space[:, np.newaxis] - phase_space[np.newaxis, :]) ** 2,
                    axis=2,
                )
            )
            < threshold
        )

        recurrence_rate = np.sum(rec_matrix) / (N**2)
        diag_lens = [np.sum(np.diag(rec_matrix, k)) for k in range(1, N)]
        det = np.sum(np.array(diag_lens) > 1) / np.sum(diag_lens)
        laminarity = np.sum(diag_lens) / N

        return {
            "recurrence_rate": recurrence_rate,
            "determinism": det,
            "laminarity": laminarity,
        }
