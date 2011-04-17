uniform sampler2D blades;
varying vec3 lightVec[4];
varying vec3 N;

void main(void) { 
	vec4 grassSample = texture2D(blades, gl_TexCoord[0].xy);

    //calculate Diffuse Term:  
	float distSqr = dot(lightVec[0], lightVec[0]);
	vec3 lVec = lightVec[0] * inversesqrt(distSqr);
	float diffuse = max(dot(N, lVec),0.0);
	vec3 color0 = diffuse * grassSample.rgb * gl_LightSource[0].diffuse.rgb;

	float invRadius = 0.010;
	vec4 tempColor = {0,0,0,0};

	int i;
	for(i = 1; i < 4; i++)
	{
		distSqr = dot(lightVec[i], lightVec[i]);
		float att = clamp(1.0 - invRadius * sqrt(distSqr), 0.0, 1.0);
		vec3 lVec1 = lightVec[i] * inversesqrt(distSqr);
		diffuse = max( dot(lVec1, N), 0.0 );
		vec4 vDiffuse = gl_LightSource[i].diffuse * diffuse;	
		tempColor = ((vDiffuse * grassSample) * att) + tempColor;
	}

	gl_FragColor = vec4(color0.rgb + tempColor.rgb, grassSample.a);
}

