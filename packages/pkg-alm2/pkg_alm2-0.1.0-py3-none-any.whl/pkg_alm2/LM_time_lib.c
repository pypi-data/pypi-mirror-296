/*
###########################################
#   Copyright (C) 2024 Mauro Migliardi
# 	This file contains the functions that provide the C implementation of the LM technique 
#   for estimating the log-likelihood of the Dirichlet Multinomial Distribution
###########################################
#   This software is licensed under the GNU General Public License version 3 (GPL-3), as published by the Free Software Foundation.
#   You can find a copy of the license at https://www.gnu.org/licenses/gpl-3.0.en.html
########################################################
*/
#define _USE_MATH_DEFINES
#include <stdio.h>
#include <sys/time.h>
#include <stdlib.h>
#include <math.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include "constants_hor_shift.h"
#include "LM_hor_shift.h"
#include "init_hor_shift.h"

//auxiliary functions  to make Minka's fixed-point iteration easier to code
void update_psioverprobs(double freshpsioverprobs[])
{
	for(int i = 0; i < K ; i++)
		psioverprobs[i] = freshpsioverprobs[i];
}

void initBern_logL()
{
	FILE* f2 = fopen("bernreal-norm-100.txt", "r");
	FILE* f4 = fopen("err_coeff-100.txt", "r");
	int i = 0;
	vec_evenbernoullinorm = (double*)malloc(100*sizeof(double));
	vec_errcoeff = (double*)malloc(100*sizeof(double));

	for(i=0;i<100;i++)
	{
		int f = fscanf(f2, "%lf", &(vec_evenbernoullinorm[i]));
		int ff = fscanf(f4, "%lf", &(vec_errcoeff[i]));
	}

	fclose(f2);
	fclose(f4);

	for(i=0;i<2;i++)
	{
		vect_logL[i] = 0;
	}
}

// computation of logL
double LM_logL(double x, double y, long m, int hor_shift)
{
	double retval = 0;
	long i = 0;
	long j = 0;

	/* inderted by AL 23/04/2023 */
	/* special values */
	if (y == 1)
		{
		retval = -log(x);
		return retval;
		}
	if (y == 2)
		{
		retval = log((1.0 + x)/(x*x));
		return retval;
		}

	/* handling the horizontal shift contribution; see LM-paper, eq. (12)	*/

	double hor_shift_contrib = 0;
	if (hor_shift != 0)
		{
		double oneoverx = 1.0 / x;
		hor_shift_contrib = log(oneoverx);
		/* computing the horizontal shift contribution */
		for(j = 1 ; j < hor_shift; j++)
			{
			hor_shift_contrib += log(oneoverx + j);
			}
		/* performing the horizontal shift */
		y = y - hor_shift;
		x = 1.0 / ( oneoverx + hor_shift );
		}
	/* now x and y are NEW: contain the horizontal shift corrections */
	double yminusone = y - 1.0;
	double d = 1.0 / (1.0 + x * yminusone );

	double	stepx = x * x;
	double	stepd = d * d;

	double	fattorex = x;
	double	fattored = d;

	retval = -y * log(x) - yminusone - (1.0/x + y - 0.5) * log(d);
	retval += vec_evenbernoullinorm[0] * fattorex * ( - 1.0 + fattored );

	for(i = 1; i < m; i++)
		{
			fattorex = fattorex * stepx;
			fattored = fattored * stepd;
			retval += vec_evenbernoullinorm[i] * fattorex * ( - 1.0 + fattored );
		}

		/* adding the horizontal shift contribution */
	retval = retval + hor_shift_contrib;
	return retval;
}

double logL_diretta(long m, int hor_shift)
{
	//printf("N = %f\n", N);
	double retval = -LM_logL(psi, N, m, hor_shift);
	long i = 0;
	for ( i = 0; i < K; i++)
	{
		retval += LM_logL(psioverprobs[i], X[i], m, hor_shift);
	}
	return retval;
}

//Utilizes m_gloabl and hor_shift_gloabl
double logL_diretta_global()
{
	double retval = -LM_logL(psi, N, m_global, hor_shift_global);
	long i = 0;
	for ( i = 0; i < K; i++)
	{
		retval += LM_logL(psioverprobs[i], X[i], m_global, hor_shift_global);
	}
	return retval;
}


long* opterrNoPrint_logL(long *maxprec, double *toterr, double n)
{
	long m = 0;
	long i = 0;
	double toterr1;
	int hor_shift = 0;
	int max_hor_shift = 1000;
	int ok = 0;
	int j = 0;
	long m_opt = 0;
	long expo = 0;
	double coeff = 0;
	double aux_psi = 0;
	double aux_psioverprobs = 0;
	double psi_pow = 0;
	double step_psi = 0;
	double* psioverprobs_pow;
	psioverprobs_pow = (double*)malloc(K*sizeof(double));
	double* step_psioverprobs;
	step_psioverprobs = (double*)malloc(K*sizeof(double));
	long counter = 0;

	while (ok == 0 && j < max_hor_shift)
	{
		// *************	begin comput. error for m=1
		counter += 1;
		m = 1;
		expo = 3;
		// coeff m of the vec_errcoeff is stored in position m-1
		coeff = vec_errcoeff[m-1];
		// for the horizontal shift; first category
		aux_psi = psi / (1.0 + j * psi);
		// step for the repeated product strategy for the next values
		step_psi = aux_psi * aux_psi;
		// start for the repeated product strategy for the next values
		psi_pow = step_psi * aux_psi;
		// contribution of the first term
		*toterr = coeff * psi_pow;
		for(i = 0; i < K; i++)
		{
		
			// for the horizontal shift; other categories
			aux_psioverprobs = psioverprobs[i] / ( 1.0 + j * psioverprobs[i]);
			// step for the repeated product strategy
			step_psioverprobs[i] = aux_psioverprobs * aux_psioverprobs;
			//psioverprobs_pow[i] = pow(aux_psioverprobs, expo);
			// start for the repeated product strategy
			psioverprobs_pow[i] = step_psioverprobs[i] * aux_psioverprobs;
			// contribution of the subsequent terms
			*toterr += coeff * psioverprobs_pow[i];
		}

		// ************* end comput. error for m=1

		//*************	begin comput. error for m=2
	
		m += 1;
		//coeff m of the vec_errcoeff is stored in position m-1
		coeff = vec_errcoeff[m-1];
		psi_pow *= step_psi;
		toterr1 = coeff * psi_pow;
		for(i = 0; i < K; i++)
		{
			/* for the horizontal shift */
			psioverprobs_pow[i] *= step_psioverprobs[i];
			toterr1 += coeff * psioverprobs_pow[i];
		}

		// ************* end comput. error for m=2


		while ( toterr1 < *toterr && *toterr > LM_accuracy && m < 100)
		{
			*toterr = toterr1;
			// *************	begin comput. error for the next m
			m += 1;
			// coeff m of the vec_errcoeff is stored in position m-1
			coeff = vec_errcoeff[m-1];
			psi_pow *= step_psi;
			toterr1 = coeff * psi_pow;
			for(i = 0; i < K; i++)
			{
				/* for the horizontal shift */
				psioverprobs_pow[i] *= step_psioverprobs[i];
				toterr1 += coeff * psioverprobs_pow[i];
			}
			counter += 1;
			// ************** end comput. error for the next m
		}

		if (*toterr < LM_accuracy)
		{
			ok = 1;
			hor_shift = j; /* horizontal shift for this accuracy */
			if (m <= 100)
			{
				m_opt = m-1; /* optimal m for this accuracy*/
			}
			else
			{
				m_opt = 100; /* optimal m for this accuracy*/
			}
		}
		j += 1;
	}
	if (ok == 0)
	{
		printf("Horizontal shift [logL] too large (>1000) for the required accuracy; ask for a smaller accuracy");
		vect_logL[0] = 0;
		vect_logL[1] = 0;
		return vect_logL;
	}

	*maxprec = floor(fabs(log10((K+1.0) * (*toterr)))) -1;

	vect_logL[0] = m_opt;
	vect_logL[1] = hor_shift;
	return vect_logL;
}



long init_params(int PREC, double counts[], int categories ){
	//initializes: K(number of categories) , X (vector of counts), and (N) total counts , PRECISION(equal to prec, by Sherenaz), LM_accuracy, SIGDIG
	//allocates memory for X, probs, psioverprobs, and logprobs

	long i = 0;
	K = categories;
	N = 0;
	long NN=0;
	PRECISION = PREC;
	SIGDIG = 15; // meaningful digits for the double type
	//SIGDIG = 19; // mea ningful digits for the longdouble type

	// we divide by (K+1) since we want that the total error has prec decimal digits correct
	LM_accuracy = pow(10, -(PREC+2));
	LM_accuracy = LM_accuracy / (K + 1.0) ;

	//allocate vector X, and other vectors
	X = (double*)malloc(K*sizeof(double));
 	probs = (double*)malloc(K*sizeof(double));
 	psioverprobs = (double*)malloc(K*sizeof(double));
 	logprobs = (double*)malloc(K*sizeof(double));

	//fillup only vector X, and integral N
	for(i = 0; i < K ; i++){
		X[i] = counts[i];
		N += X[i];
		//NN+=X[i];
	}
	return NN;
}

double loggamma_LM( double probabilities[],  double psi_0)
	//to refresh probs and psi before each call to loggamma_LM
{
	double pown = 0;
	long i = 0;
 	//refresh psi, probs, and psioverprobs
	psi = psi_0;
	for(i = 0; i < K ; i++){
		//probs[i] = probabilities[i];
		psioverprobs[i] = psi/probabilities[i];
		logprobs[i] = log(probabilities[i]);

	}


	//reset asymp
	asymp = 0;

	for(i=0;i<K;i++)
	{
		asymp += logprobs[i] * X[i];
	}

	//must be done before every call to loggamma_LM
	double bound = SIGDIG - PRECISION -2 ;
	if ( log10(fabs(asymp)) > bound)
	{
		printf("N = %f\nK = %ld\n",	N, K);
 		printf("logL of this case is asymptotic to (psi -> 0+) = %32.30f\n", asymp);
	 	fprintf(stderr, "ERROR: LogL too large to assure the desired precision in double; switch to multiprecision\n");
		printf("***** END PROGRAM *****\n");
		return 99;
	}



	double toterr;
	long maxprec;
	int hor_shift_logL = 0;
 	long acc_logL = 0;
 	double toterr_logL = 0;
 	long opt_m_logL = 0;
	double res_logL = 0;

	opterrNoPrint_logL(&maxprec, &toterr, pown);


	acc_logL = maxprec;
	toterr_logL = toterr;

	m_global = vect_logL[0];
	hor_shift_global = vect_logL[1];

	res_logL = logL_diretta_global();
	return res_logL;
}
