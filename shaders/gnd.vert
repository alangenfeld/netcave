varying vec3 lightVec[4]; 
varying vec2 texCoord;

void main(void)
{
	vec3 tangent;
	vec3 binormal;

	vec3 c1 = cross( gl_Normal, vec3(0.0, 0.0, 1.0) );
	vec3 c2 = cross( gl_Normal, vec3(0.0, 1.0, 0.0) );

	if( length(c1)>length(c2) )
	{
		tangent = c1;	
	}
	else
	{
		tangent = c2;
	}

	tangent = normalize(tangent);

	binormal = cross(gl_Normal, tangent);
	binormal = normalize(binormal);
	
	gl_Position = ftransform();
	texCoord = gl_MultiTexCoord0.xy;
	
	vec3 n = normalize(gl_NormalMatrix * gl_Normal);
	vec3 t = normalize(gl_NormalMatrix * tangent);
	vec3 b = cross(n, t);
	
	vec3 vVertex = vec3(gl_ModelViewMatrix * gl_Vertex);

	int	i;
	vec3 tmpVec;
	
	for(i = 0; i < 4; i++)
	{
		tmpVec = gl_LightSource[i].position.xyz - vVertex;

		lightVec[i].x = dot(tmpVec, t);
		lightVec[i].y = dot(tmpVec, b);
		lightVec[i].z = dot(tmpVec, n);
	}
}
