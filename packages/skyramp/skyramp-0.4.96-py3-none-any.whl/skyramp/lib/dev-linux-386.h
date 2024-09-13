/* Code generated by cmd/cgo; DO NOT EDIT. */

/* package github.com/letsramp/dev/cmd/libs */


#line 1 "cgo-builtin-export-prolog"

#include <stddef.h>

#ifndef GO_CGO_EXPORT_PROLOGUE_H
#define GO_CGO_EXPORT_PROLOGUE_H

#ifndef GO_CGO_GOSTRING_TYPEDEF
typedef struct { const char *p; ptrdiff_t n; } _GoString_;
#endif

#endif

/* Start of preamble from import "C" comments.  */


#line 7 "client.go"

struct oauthresponse {
    char *emails[10];    // for the time being, it is a bit tricky to deal with dynamic array with koffi
    int   num_emails;
    char *token;
    char *error;
};

struct credential_response {
    char *email;
    char *user_token;
    char *provider;
    char *error;
};

struct worker_info {
    char *container_name;
    char *error;
};

#line 1 "cgo-generated-wrapper"

#line 7 "endpoint.go"

	struct tester_info {
	    char *tester_id;
	    char *error;
	};

#line 1 "cgo-generated-wrapper"


/* End of preamble from import "C" comments.  */


/* Start of boilerplate cgo prologue.  */
#line 1 "cgo-gcc-export-header-prolog"

#ifndef GO_CGO_PROLOGUE_H
#define GO_CGO_PROLOGUE_H

typedef signed char GoInt8;
typedef unsigned char GoUint8;
typedef short GoInt16;
typedef unsigned short GoUint16;
typedef int GoInt32;
typedef unsigned int GoUint32;
typedef long long GoInt64;
typedef unsigned long long GoUint64;
typedef GoInt32 GoInt;
typedef GoUint32 GoUint;
typedef size_t GoUintptr;
typedef float GoFloat32;
typedef double GoFloat64;
#ifdef _MSC_VER
#include <complex.h>
typedef _Fcomplex GoComplex64;
typedef _Dcomplex GoComplex128;
#else
typedef float _Complex GoComplex64;
typedef double _Complex GoComplex128;
#endif

/*
  static assertion to make sure the file is being used on architecture
  at least with matching size of GoInt.
*/
typedef char _check_for_32_bit_pointer_matching_GoInt[sizeof(void*)==32/8 ? 1:-1];

#ifndef GO_CGO_GOSTRING_TYPEDEF
typedef _GoString_ GoString;
#endif
typedef void *GoMap;
typedef void *GoChan;
typedef struct { void *t; void *v; } GoInterface;
typedef struct { void *data; GoInt len; GoInt cap; } GoSlice;

#endif

/* End of boilerplate cgo prologue.  */

#ifdef __cplusplus
extern "C" {
#endif

extern char* removeLocalWrapper();
extern char* removeClusterFromConfigWrapper(char* clusterName);
extern char* getKubeConfigPath();
extern char* applyLocalWrapper();
extern char* addKubeconfigWrapper(char* context, char* clusterName, char* kubeconfigPath);
extern char* setProjectDirectoryWrapper(char* context);
extern char* getEndpointFromProjectWrapper(char* endpointName, char* projectPath);
extern char* deployTargetWrapper(char* filePath, char* namespace, char* kubePath, char* kubeContext, char* clusterName, char* workerImage, GoUint8 localImage);
extern char* deploySkyrampWorkerWrapper(char* namespace, char* kubePath, char* kubeContext, char* clusterName, char* workerImage, GoUint8 localImage);
extern char* deleteTargetWrapper(char* filePath, char* namespace, char* kubePath, char* kubeContext, char* clusterName);
extern char* deleteSkyrampWorkerWrapper(char* namespace, char* kubePath, char* kubeContext, char* clusterName);
extern char* initTargetWrapper(char* fileName);
extern struct credential_response readCredentialWrapper();
extern char* getOAuthURLWrapper(char* provider, GoInt port);
extern char* registerUserWrapper(char* provider, char* email, char* code);
extern struct oauthresponse runOAuthLoopback(char* provider, GoInt port);
extern char* validateTokenWrapper(char* userToken);
extern char* generateUserTokenWrapper(char* provider, char* email, char* oauthToken);
extern struct worker_info newStartDockerSkyrampWorkerWrapper(char* image, char* tag, GoInt hostPort, char* targetNetworkName, char* testServiceAlias);
extern char* newDeleteDockerSkyrampWorkerWrapper(char* containerName);
extern char* runTesterCurlWrapper(char* namespace, char* kubePath, char* kubeContext, char* clusterName, char* address, char* request);
extern char* newGrpcEndpointWrapper(char* name, char* serviceName, GoInt port, char* inputFile);
extern char* newRestEndpointWrapper(char* name, char* openApiTag, GoInt port, char* inputFile, char* restPath);
extern char* getEndpointWrapper(char* service, GoInt port, char* restPath);
extern char* writeMockDescriptionWrapper(char* mockDescription, char* kubernetesService);
extern char* writeTestDescriptionWrapper(char* testDescription, char* testName);
extern char* applyMockDescriptionWrapper(char* namespace, char* kubePath, char* kubeContext, char* clusterName, char* address, char* mockDescription, char* mockPath, char* projectPath);
extern char* buildRequestsWrapper(char* mockDescription);
extern struct tester_info runTesterStartWrapper(char* namespace, char* kubePath, char* kubeContext, char* clusterName, char* address, char* testDescription, GoUint8 generateResult);
extern struct tester_info runTesterStartWrapperWithGlobalHeaders(char* namespace, char* kubePath, char* kubeContext, char* clusterName, char* address, char* testDescription, char* testFileName, char* testName, char* globalJsonHeaders, GoUint8 generateResult, char* projectPath, char* overrideFile, char* overrideDict);
extern char* runTesterStatusWrapper(char* namespace, char* kubePath, char* kubeContext, char* clusterName, char* address, char* testerId, GoUint8 isFormattingEnabled);

#ifdef __cplusplus
}
#endif
