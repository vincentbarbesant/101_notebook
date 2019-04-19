function mpc = reference_grid14
%REFERENCE_GRID14

%% MATPOWER Case Format : Version 2
mpc.version = '2';

%%-----  Power Flow Data  -----%%
%% system MVA base
mpc.baseMVA = 100;

%% bus data
%	bus_i	type	Pd	Qd	Gs	Bs	area	Vm	Va	baseKV	zone	Vmax	Vmin
mpc.bus = [
	1	3	0	0	0	0	1	1.02	0	100	1	1.03	0.97;
	2	2	0	0	0	0	1	1.01	0	100	1	1.03	0.97;
	3	1	2       -1.2	0	0	1	1.00	0	100	1	1.03	0.97;
	4	1	3	-0.2	0	0	1	1.01	0	100	1	1.03	0.97;
        6661    4       0       0       0       0       1       1.01    0       100     1       1.03    0.97;
        6662    4       0       0       0       0       1       1.01    0       100     1       1.03    0.97;
        6663    4       0       0       0       0       1       1.01    0       100     1       1.03    0.97;
        6664    4       0       0       0       0       1       1.01    0       100     1       1.03    0.97;
];

%% generator data
%	bus	Pg	Qg	Qmax	Qmin	Vg	mBase	status	Pmax	Pmin	Pc1	Pc2	Qc1min	Qc1max	Qc2min	Qc2max	ramp_agc	ramp_10	ramp_30	ramp_q	apf
mpc.gen = [
	1	10	10	100	-100	1.02	100	1	332.4	0	0	0	0	0	0	0	0	0	0	0	0;
	2	10	10	50	-50	1.01	100	1	140	0	0	0	0	0	0	0	0	0	0	0	0;
];

%% branch data
%	fbus	tbus	r	x	b	rateA	rateB	rateC	ratio	angle	status	angmin	angmax
mpc.branch = [
	1	2	0.05938	0.05917	0.0528	0	0	0	0	0	1	-360	360;
	1       3	0.05403	0.22304	0.0492	0	0	0	0	0	1	-360	360;
	1	4	0.03699	0.19797	0.0438	0	0	0	0	0	1	-360	360;
	2	4	0.05811	0.17632	0.034	0	0	0	0	0	1	-360	360;
	3	4	0.06701	0.17103	0.0128	0	0	0	0	0	1	-360	360;
];
