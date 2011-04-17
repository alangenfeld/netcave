uniform float time;
uniform float wind;
void main(void) 
{ 
	vec4 tempPos = gl_Vertex;
	if(tempPos.y > 0.2) 
     { 
		float cosine = (cos(time * 0.03)) * (gl_MultiTexCoord0.y)*(gl_MultiTexCoord0.y) * wind;
  		tempPos.x += cosine;
  		tempPos.z += cosine;
     }
	gl_TexCoord[0] = gl_MultiTexCoord0;
	gl_Position = gl_ModelViewProjectionMatrix * tempPos;
}
