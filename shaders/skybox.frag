uniform sampler2D skybox;
uniform float timeOfDay;

void main(void) 
{
	float colorScale = 0.07*abs(12-timeOfDay);
	vec4 texSample = texture2D(skybox, gl_TexCoord[0].xy);
	gl_FragColor = vec4(texSample.r -= texSample.r*colorScale, texSample.g -= texSample.g*colorScale, texSample.b -= texSample.b*colorScale, texSample.a);
}