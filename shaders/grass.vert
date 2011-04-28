uniform float time;
uniform float wind;
varying vec3 lightVec[4];
varying vec3 N;

void main(void) 
{ 
	N = normalize(gl_NormalMatrix * gl_Normal);

	vec4 tempPos = gl_Vertex;
	if(tempPos.y > 0.2) 
     { 
		float cosine = (cos(time * 0.03)) * (gl_MultiTexCoord0.y)*(gl_MultiTexCoord0.y) * wind;
  		tempPos.x += cosine;
  		tempPos.z += cosine;
     }
	gl_TexCoord[0] = gl_MultiTexCoord0;
	gl_Position = gl_ModelViewProjectionMatrix * tempPos;

	vec3 tmpVec = vec3(gl_ModelViewMatrix * tempPos);

	int i;
	for(i = 0; i < 4; i++)
	{
		lightVec[i] = gl_LightSource[i].position.xyz - tmpVec;
	}

}
