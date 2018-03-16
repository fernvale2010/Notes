
// http://www.retinatronics.com/using-kalman-filter-for-analogue-to-digital-measurements/

unsigned int Kalman_filter_for_SEN_1(signed int ADC_Value)
{
	static unsigned char counter = 0;
	static float A,H,Q,R,X,P;
	float XP,PP;
	static float value_return=0;
	float K;
	float temp_float;

	if(counter<1)
		counter++;

	if(counter==1)
	{
		A = 1;
		H = 1;   //1
		Q = 0.32;     //earlier 0.92,0.02
		R = 0.8;     //
		X = 1023;
		P = 6;
		counter = 2;

		XP = A*X;
		PP = A*P*A + Q;

		K = PP*H;
		K /=(H*H*PP)+R;

		temp_float = (float)(ADC_Value-H*XP);
		value_return = XP + K*temp_float;

		temp_float = H*PP;
		P = PP-K*temp_float;
		return (unsigned int)value_return;
	}
	else
	{
		XP = A*value_return;
		PP = A*P*A + Q;

		K = PP*H;
		K /=(H*H*PP)+R;

		temp_float = (float)(ADC_Value-H*XP);
		value_return = XP + K*temp_float;

		temp_float = (float)H*PP;
		P = PP-K*temp_float;
		return (unsigned int)value_return;

	}

}

