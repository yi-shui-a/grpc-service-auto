/****************************************************************

  Generated by Eclipse Cyclone DDS IDL to C Translator
  File name: /root/atom_service_dev/server_compiling/db/client/test0521/idl/StartRequest/StartRequest.h
  Source: /root/atom_service_dev/server_compiling/db/client/test0521/idl/StartRequest/StartRequest.idl
  Cyclone DDS: V0.11.0

*****************************************************************/
#ifndef DDSC__ROOT_ATOM_SERVICE_DEV_SERVER_COMPILING_DB_CLIENT_TEST0521_IDL_STARTREQUEST_STARTREQUEST_H_CF4B5598538E233FC547F33D470F4CE9
#define DDSC__ROOT_ATOM_SERVICE_DEV_SERVER_COMPILING_DB_CLIENT_TEST0521_IDL_STARTREQUEST_STARTREQUEST_H_CF4B5598538E233FC547F33D470F4CE9

#include "dds/ddsc/dds_public_impl.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct StartRequest_atomic_service_mbsb_task_A_Request_st
{
  int32_t number1;
  int32_t number2;
} StartRequest_atomic_service_mbsb_task_A_Request_st;

extern const dds_topic_descriptor_t StartRequest_atomic_service_mbsb_task_A_Request_st_desc;

#define StartRequest_atomic_service_mbsb_task_A_Request_st__alloc() \
((StartRequest_atomic_service_mbsb_task_A_Request_st*) dds_alloc (sizeof (StartRequest_atomic_service_mbsb_task_A_Request_st)));

#define StartRequest_atomic_service_mbsb_task_A_Request_st_free(d,o) \
dds_sample_free ((d), &StartRequest_atomic_service_mbsb_task_A_Request_st_desc, (o))

#ifdef __cplusplus
}
#endif

#endif /* DDSC__ROOT_ATOM_SERVICE_DEV_SERVER_COMPILING_DB_CLIENT_TEST0521_IDL_STARTREQUEST_STARTREQUEST_H_CF4B5598538E233FC547F33D470F4CE9 */
