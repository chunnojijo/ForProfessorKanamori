#include <gl/glut.h>
#include <iostream>
#include<math.h>
#include <iostream>
#include <cmath>
#include <list>
#include<string> 
#include <sstream>

// 光源 (環境光､拡散光､鏡面光､位置) のパラメータ
GLfloat lightAmb[] = { 0.0, 0.0, 0.0, 1.0 };
GLfloat lightDiff[] = { 1.0, 1.0, 1.0, 1.0 };
GLfloat lightSpec[] = { 1.0, 1.0, 1.0, 1.0 };
GLfloat lightPos[] = { 3.0, 3.0,3.0, 0.0 };  // 平行光源

//材質 (環境光､拡散光､鏡面光､鏡面指数) のパラメータ（金）
GLfloat goldAmb[] = { 0.24725f, 0.1995f, 0.0745f, 1.f };
GLfloat goldDiff[] = { 0.75164f, 0.60648f , 0.22648f, 1.f };
GLfloat goldSpec[] = { 0.628281f, 0.555802f,0.366065f,1.f };
GLfloat goldShin = 51.2f;

int allTime = 0;
int wallInstantiateSpan = 180;
int speedUpSpan = 180;
const float CAMERA_Z = 0;
float cameraX = 0;
float cameraY = 0;
float currentCameraX = 0;
float currentCameraY = 0;
const float INITIAL_SPEED = 0.3;
const float MAX_SPEED = 1;
bool isPushedW = false;
bool isPushedA = false;
bool isPushedS = false;
bool isPushedD = false;
bool isGameOver = false;

class Wall {
public:
	Wall() {
		spot = std::rand() % 9;
	}
	Wall(float speed) {
		this->speed = speed;
		spot = std::rand() % 9;
	}
	int spot = 0;//0～8
	float speed = INITIAL_SPEED;
	float z = -160;
	bool isPlacedCamera = false;
	void Show() {
		for (int x = -1; x <= 1; x++) {
			for (int y = -1; y <= 1; y++) {
				if (x == (spot / 3 - 1) && y == (spot % 3 - 1)) {
					continue;
				}
				glPushMatrix();
				glTranslated(x * 2, y * 2, z);
				glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, goldAmb);
				glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, goldDiff);
				glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, goldSpec);
				glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, goldShin);
				glutSolidSphere(1, 30, 30);
				glPopMatrix();
			}
		}
	}
	void Proceed() {
		z += speed;
	}
	bool AbleToSee() {
		return z < CAMERA_Z - 2;
	}
	bool IsHit(float x, float y) {
		/*if (z > -1 || z < -2) {
			return false;
		}*/
		if (z <-2) {
			return false;
		}
		if (z > -1) {
			if (!isPlacedCamera) {
				isPlacedCamera = true;
			}
			else {
				return false;
			}
		}
		if (z<-1 && z>-2) {
			isPlacedCamera = true;
		}

		int spotX = (spot / 3 - 1);
		int spotY = (spot % 3 - 1);

		return !((spotX * 2 + 1) > x && (spotX * 2 - 1) < x && (spotY * 2 + 1) > y && (spotY * 2 - 1) < y);
	}
};

std::list<Wall> walls;

void InitializeVariable() {
	walls.clear();
	allTime = 0;
	wallInstantiateSpan = 180;
	speedUpSpan = 180;
	cameraX = 0;
	cameraY = 0;
	currentCameraX = 0;
	currentCameraY = 0;
	isGameOver = false;
}

float lerp(float a, float b, float t) {
	return a + t * (b - a);
}
void ShowUI() {
	std::list<Wall>::iterator wallItr;
	int scoreCount = 0;
	for (wallItr = walls.begin(); wallItr != walls.end(); wallItr++) {
		if (!wallItr->AbleToSee()) {
			scoreCount++;
		}
	}
	char numstr[21];
	sprintf_s(numstr, "%d", scoreCount);
	std::string scoreString = "Score";
	std::string score = scoreString + numstr;

	int size = (int)score.size();
	for (int i = 0; i < size; ++i) {
		glRasterPos3f(0.2f + i * 0.01f, 0.2f, -1);
		char ic = score[i];
		glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ic);
	}
	if (isGameOver) {
		glColor3d(245, 0, 0);
		std::string gameOverString = "GameOver";
		for (int i = 0; i < (int)gameOverString.size(); ++i) {
			glRasterPos3f(i * 0.03f - 0.1f, 0, -1);
			char ic = gameOverString[i];
			glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ic);
		}

		std::string continueString = "Continue To Push ESC";
		for (int i = 0; i < (int)continueString.size(); ++i) {
			glRasterPos3f(i * 0.03f - 0.26f, -0.05, -1);
			char ic = continueString[i];
			glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ic);
		}
	}
}

void SetGameOverBool() {
	bool result = false;
	std::list<Wall>::iterator itr;
	for (itr = walls.begin(); itr != walls.end(); itr++) {
		if (itr->IsHit(currentCameraX, currentCameraY)) {
			result = true;
			continue;
		}
	}
	if (result) {
		isGameOver = true;
	}
}

void SetCameraPosition() {
	currentCameraX = lerp(currentCameraX, cameraX, 0.3f);
	currentCameraY = lerp(currentCameraY, cameraY, 0.3f);
	cameraY = 0;
	cameraX = 0;
	if (isPushedW) {
		cameraY += 2;
	}
	if (isPushedS) {
		cameraY -= 2;
	}
	if (isPushedA) {
		cameraX -= 2;
	}
	if (isPushedD) {
		cameraX += 2;
	}
}

//--------- 各種コールバック関数-------//
void display(void) {
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glLoadIdentity();

	ShowUI();

	gluLookAt(currentCameraX, currentCameraY, CAMERA_Z, currentCameraX, currentCameraY, -1.0, 0.0, 1.0, 0.0);

	//光源の位置設定
	glLightfv(GL_LIGHT0, GL_POSITION, lightPos);

	//材質設定と描画

	std::list<Wall>::iterator itr;
	for (itr = walls.begin(); itr != walls.end(); itr++) {
		if (itr->AbleToSee()) {
			itr->Show();
		}
	}

	glFlush();	// 命令の実行
}

void timer(int value)
{
	int time = value;
	if (!isGameOver) {
		allTime++;
		if (time > wallInstantiateSpan) {
			time = 0;
			float speed = INITIAL_SPEED + 0.0001*allTime;
			if (speed > MAX_SPEED) {
				speed = MAX_SPEED;
			}

			walls.push_back(Wall(INITIAL_SPEED + 0.0005*allTime));

		}

		if (allTime%speedUpSpan == 0) {
			wallInstantiateSpan -= 13;
			if (wallInstantiateSpan < 43) {
				wallInstantiateSpan = 43;
			}
		}
		std::list<Wall>::iterator itr;
		std::list<Wall> removeList;
		for (itr = walls.begin(); itr != walls.end(); itr++) {
			itr->Proceed();
		}
	}
	glutPostRedisplay();

	SetCameraPosition();

	SetGameOverBool();
	glutTimerFunc(15, timer, time + 1);    // 15ミリ秒後にまたタイマー関数を呼ぶ
}
void reshape(int w, int h) {
	glViewport(0, 0, w, h);

	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	gluPerspective(30.0, double(w) / h, 0.1, 200.0);

	glMatrixMode(GL_MODELVIEW);
}
void key(unsigned char key, int x, int y) {
	if (key == 'w') {
		isPushedW = true;
	}

	if (key == 'a') {
		isPushedA = true;
	}

	if (key == 's') {
		isPushedS = true;
	}

	if (key == 'd') {
		isPushedD = true;
	}
	if (isGameOver&&key == '\033') {
		InitializeVariable();
	}
}

void key2(unsigned char key, int x, int y) {
	if (key == 'w') {
		isPushedW = false;
	}
	if (key == 'a') {
		isPushedA = false;
	}

	if (key == 's') {
		isPushedS = false;
	}

	if (key == 'd') {
		isPushedD = false;
	}
}


//--------- 各種設定-----------//
void Init(void) {
	glClearColor(1.0, 1.0, 1.0, 1.0);
	glClearDepth(1.0);
	glEnable(GL_DEPTH_TEST);

	//光源設定(環境､拡散､鏡面のみ)
	glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmb);
	glLightfv(GL_LIGHT0, GL_DIFFUSE, lightDiff);
	glLightfv(GL_LIGHT0, GL_SPECULAR, lightSpec);

	//光源とライティング有効化
	glEnable(GL_LIGHT0);
	glEnable(GL_LIGHTING);
}

//---------- メイン関数-------------//
int main(int argc, char *argv[]) {
	walls.push_back(Wall());
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH);
	glutInitWindowSize(640, 480);
	glutCreateWindow("Light and Material");

	//コールバック関数登録
	glutDisplayFunc(display);
	glutReshapeFunc(reshape);
	glutTimerFunc(0, timer, 1);
	//glutMouseFunc(mouse);
	glutKeyboardFunc(key);
	glutKeyboardUpFunc(key2);

	Init();

	glutMainLoop();

	return 0;
}