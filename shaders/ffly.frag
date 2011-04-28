uniform sampler2D glow;
uniform float time;

void main(void) { 
 float cosine = (cos(time * 0.03)) + 1;
 
 vec4 glowSample = texture2D(glow, gl_TexCoord[0].xy);
 gl_FragColor = vec4(glowSample.rgb, glowSample.a*(cosine*(0.5)));
 //gl_FragColor = glowSample;
}