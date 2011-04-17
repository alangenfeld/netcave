
uniform sampler2D colorMap;
uniform sampler2D normalMap;
varying vec3 lightVec[4];
varying vec3 eyeVec[4];

void main (void)
{
	// DIFFUSE LIGHT 0
	float distSqr = dot(lightVec[0], lightVec[0]);
	vec3 lVec0 = lightVec[0] * inversesqrt(distSqr);
	vec4 base = texture2D(colorMap, gl_TexCoord[0]);
	vec3 bump = normalize( texture2D(normalMap, gl_TexCoord[0]).xyz * 2.0 - 1.0);
	float diffuse = max( -dot(lVec0, bump), 0.0 );
	vec4 vDiffuse = gl_LightSource[0].diffuse * diffuse;	
	vec3 vVec = normalize(eyeVec[0]);
	float specular = pow(clamp(dot(reflect(-lVec0, bump), vVec), 0.0, 1.0), .25);
		       
    vec4 vSpecular = gl_LightSource[0].specular * specular;		       

	vec4 tempColor0 = ( vDiffuse*base + vSpecular );


	// LOCAL LIGHT 1-3
	vec4 tempColor = {0,0,0,0};
	float invRadius = 0.010;

	int i;
	for(i = 1; i < 4; i++)
	{
		distSqr = dot(lightVec[i], lightVec[i]);
		float att = clamp(1.0 - invRadius * sqrt(distSqr), 0.0, 1.0);
		vec3 lVec1 = lightVec[i] * inversesqrt(distSqr);
		diffuse = max( -dot(lVec1, bump), 0.0 );
		vDiffuse = gl_LightSource[i].diffuse * diffuse;	
		vVec = normalize(eyeVec[i]);
		specular = pow(clamp(dot(reflect(-lVec1, bump), vVec), 0.0, 1.0), .25);	
		vSpecular = gl_LightSource[i].specular * specular;		       
		
		tempColor = ((vDiffuse * base + vSpecular) * att) + tempColor;
	}

	gl_FragColor = vec4(tempColor0.rgb + tempColor.rgb, 1.0);
}

