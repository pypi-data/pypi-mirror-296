/*
###########################################
#   Copyright (C) 2024 Mauro Migliardi
# 	This is a header file for variables required for the LM_time_lib.c code
###########################################
#   This software is licensed under the GNU General Public License version 3 (GPL-3), as published by the Free Software Foundation.
#   You can find a copy of the license at https://www.gnu.org/licenses/gpl-3.0.en.html
########################################################
*/
#define LOOP 1

long m_global;
int hor_shift_global;
int SIGDIG;
int PRECISION;
double asymp;
long K; 
double* probs;
double* psioverprobs;
double* X;
double* logprobs;
double psi;
long vect_logL[2];
long vect_digamma[2];
long vect_trigamma[2];
double N;
double LM_accuracy;
double* vec_evenbernoulli;
double* vec_evenbernoullinorm;
double* vec_evenbernoullinormdigamma;
double* vec_errcoeff;

