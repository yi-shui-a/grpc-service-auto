/****************************************************************

  Generated by Eclipse Cyclone DDS IDL to C Translator
  File name: /root/atom_service_dev/server_compiling/db/client/test0521/idl/EndRequest/EndRequest.h
  Source: /root/atom_service_dev/server_compiling/db/client/test0521/idl/EndRequest/EndRequest.idl
  Cyclone DDS: V0.11.0

*****************************************************************/
#ifndef DDSC__ROOT_ATOM_SERVICE_DEV_SERVER_COMPILING_DB_CLIENT_TEST0521_IDL_ENDREQUEST_ENDREQUEST_H_C6E52096D195287AB3693AAF2456618C
#define DDSC__ROOT_ATOM_SERVICE_DEV_SERVER_COMPILING_DB_CLIENT_TEST0521_IDL_ENDREQUEST_ENDREQUEST_H_C6E52096D195287AB3693AAF2456618C

#include "dds/ddsc/dds_public_impl.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct EndRequest_atomic_service_sf_task_E_Reply_st
{
  int32_t sum_result;
  int32_t return_type;
} EndRequest_atomic_service_sf_task_E_Reply_st;

extern const dds_topic_descriptor_t EndRequest_atomic_service_sf_task_E_Reply_st_desc;

#define EndRequest_atomic_service_sf_task_E_Reply_st__alloc() \
((EndRequest_atomic_service_sf_task_E_Reply_st*) dds_alloc (sizeof (EndRequest_atomic_service_sf_task_E_Reply_st)));

#define EndRequest_atomic_service_sf_task_E_Reply_st_free(d,o) \
dds_sample_free ((d), &EndRequest_atomic_service_sf_task_E_Reply_st_desc, (o))

#ifdef __cplusplus
}
#endif

#endif /* DDSC__ROOT_ATOM_SERVICE_DEV_SERVER_COMPILING_DB_CLIENT_TEST0521_IDL_ENDREQUEST_ENDREQUEST_H_C6E52096D195287AB3693AAF2456618C */
