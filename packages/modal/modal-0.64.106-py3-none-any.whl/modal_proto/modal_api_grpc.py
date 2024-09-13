# Generated by the Modal Protocol Buffers compiler. DO NOT EDIT!
# source: modal_proto/api.proto
# plugin: __main__

import modal._utils.grpc_utils
import modal_proto.api_grpc


class ModalClientModal:

    def __init__(self, grpclib_stub: modal_proto.api_grpc.ModalClientStub) -> None:
        self.AppClientDisconnect = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.AppClientDisconnect)
        self.AppCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.AppCreate)
        self.AppDeploy = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.AppDeploy)
        self.AppDeploySingleObject = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.AppDeploySingleObject)
        self.AppDeploymentHistory = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.AppDeploymentHistory)
        self.AppGetByDeploymentName = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.AppGetByDeploymentName)
        self.AppGetLogs = modal._utils.grpc_utils.UnaryStreamWrapper(grpclib_stub.AppGetLogs)
        self.AppGetObjects = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.AppGetObjects)
        self.AppGetOrCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.AppGetOrCreate)
        self.AppHeartbeat = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.AppHeartbeat)
        self.AppList = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.AppList)
        self.AppLookup = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.AppLookup)
        self.AppLookupObject = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.AppLookupObject)
        self.AppPublish = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.AppPublish)
        self.AppRollback = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.AppRollback)
        self.AppSetObjects = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.AppSetObjects)
        self.AppStop = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.AppStop)
        self.BlobCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.BlobCreate)
        self.BlobGet = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.BlobGet)
        self.ClassCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.ClassCreate)
        self.ClassGet = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.ClassGet)
        self.ClientCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.ClientCreate)
        self.ClientHeartbeat = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.ClientHeartbeat)
        self.ClientHello = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.ClientHello)
        self.ContainerCheckpoint = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.ContainerCheckpoint)
        self.ContainerExec = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.ContainerExec)
        self.ContainerExecGetOutput = modal._utils.grpc_utils.UnaryStreamWrapper(grpclib_stub.ContainerExecGetOutput)
        self.ContainerExecPutInput = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.ContainerExecPutInput)
        self.ContainerExecWait = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.ContainerExecWait)
        self.ContainerHeartbeat = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.ContainerHeartbeat)
        self.ContainerLog = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.ContainerLog)
        self.ContainerStop = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.ContainerStop)
        self.DictClear = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.DictClear)
        self.DictContains = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.DictContains)
        self.DictContents = modal._utils.grpc_utils.UnaryStreamWrapper(grpclib_stub.DictContents)
        self.DictCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.DictCreate)
        self.DictDelete = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.DictDelete)
        self.DictGet = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.DictGet)
        self.DictGetOrCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.DictGetOrCreate)
        self.DictHeartbeat = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.DictHeartbeat)
        self.DictLen = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.DictLen)
        self.DictList = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.DictList)
        self.DictPop = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.DictPop)
        self.DictUpdate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.DictUpdate)
        self.DomainCertificateVerify = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.DomainCertificateVerify)
        self.DomainCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.DomainCreate)
        self.DomainList = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.DomainList)
        self.EnvironmentCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.EnvironmentCreate)
        self.EnvironmentDelete = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.EnvironmentDelete)
        self.EnvironmentList = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.EnvironmentList)
        self.EnvironmentUpdate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.EnvironmentUpdate)
        self.FunctionBindParams = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.FunctionBindParams)
        self.FunctionCallCancel = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.FunctionCallCancel)
        self.FunctionCallGetDataIn = modal._utils.grpc_utils.UnaryStreamWrapper(grpclib_stub.FunctionCallGetDataIn)
        self.FunctionCallGetDataOut = modal._utils.grpc_utils.UnaryStreamWrapper(grpclib_stub.FunctionCallGetDataOut)
        self.FunctionCallList = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.FunctionCallList)
        self.FunctionCallPutDataOut = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.FunctionCallPutDataOut)
        self.FunctionCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.FunctionCreate)
        self.FunctionGet = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.FunctionGet)
        self.FunctionGetCallGraph = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.FunctionGetCallGraph)
        self.FunctionGetCurrentStats = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.FunctionGetCurrentStats)
        self.FunctionGetDynamicConcurrency = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.FunctionGetDynamicConcurrency)
        self.FunctionGetInputs = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.FunctionGetInputs)
        self.FunctionGetOutputs = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.FunctionGetOutputs)
        self.FunctionGetSerialized = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.FunctionGetSerialized)
        self.FunctionMap = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.FunctionMap)
        self.FunctionPrecreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.FunctionPrecreate)
        self.FunctionPutInputs = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.FunctionPutInputs)
        self.FunctionPutOutputs = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.FunctionPutOutputs)
        self.FunctionStartPtyShell = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.FunctionStartPtyShell)
        self.FunctionUpdateSchedulingParams = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.FunctionUpdateSchedulingParams)
        self.ImageGetOrCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.ImageGetOrCreate)
        self.ImageJoinStreaming = modal._utils.grpc_utils.UnaryStreamWrapper(grpclib_stub.ImageJoinStreaming)
        self.MountBuild = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.MountBuild)
        self.MountGetOrCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.MountGetOrCreate)
        self.MountPutFile = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.MountPutFile)
        self.ProxyGetOrCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.ProxyGetOrCreate)
        self.QueueClear = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.QueueClear)
        self.QueueCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.QueueCreate)
        self.QueueDelete = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.QueueDelete)
        self.QueueGet = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.QueueGet)
        self.QueueGetOrCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.QueueGetOrCreate)
        self.QueueHeartbeat = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.QueueHeartbeat)
        self.QueueLen = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.QueueLen)
        self.QueueList = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.QueueList)
        self.QueueNextItems = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.QueueNextItems)
        self.QueuePut = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.QueuePut)
        self.SandboxCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.SandboxCreate)
        self.SandboxGetLogs = modal._utils.grpc_utils.UnaryStreamWrapper(grpclib_stub.SandboxGetLogs)
        self.SandboxGetTaskId = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.SandboxGetTaskId)
        self.SandboxGetTunnels = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.SandboxGetTunnels)
        self.SandboxList = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.SandboxList)
        self.SandboxStdinWrite = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.SandboxStdinWrite)
        self.SandboxTerminate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.SandboxTerminate)
        self.SandboxWait = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.SandboxWait)
        self.SecretCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.SecretCreate)
        self.SecretGetOrCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.SecretGetOrCreate)
        self.SecretList = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.SecretList)
        self.SharedVolumeCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.SharedVolumeCreate)
        self.SharedVolumeGetFile = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.SharedVolumeGetFile)
        self.SharedVolumeGetOrCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.SharedVolumeGetOrCreate)
        self.SharedVolumeHeartbeat = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.SharedVolumeHeartbeat)
        self.SharedVolumeList = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.SharedVolumeList)
        self.SharedVolumeListFiles = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.SharedVolumeListFiles)
        self.SharedVolumeListFilesStream = modal._utils.grpc_utils.UnaryStreamWrapper(grpclib_stub.SharedVolumeListFilesStream)
        self.SharedVolumePutFile = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.SharedVolumePutFile)
        self.SharedVolumeRemoveFile = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.SharedVolumeRemoveFile)
        self.TaskCurrentInputs = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.TaskCurrentInputs)
        self.TaskList = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.TaskList)
        self.TaskResult = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.TaskResult)
        self.TokenFlowCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.TokenFlowCreate)
        self.TokenFlowWait = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.TokenFlowWait)
        self.TunnelStart = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.TunnelStart)
        self.TunnelStop = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.TunnelStop)
        self.VolumeCommit = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.VolumeCommit)
        self.VolumeCopyFiles = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.VolumeCopyFiles)
        self.VolumeCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.VolumeCreate)
        self.VolumeDelete = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.VolumeDelete)
        self.VolumeGetFile = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.VolumeGetFile)
        self.VolumeGetOrCreate = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.VolumeGetOrCreate)
        self.VolumeHeartbeat = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.VolumeHeartbeat)
        self.VolumeList = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.VolumeList)
        self.VolumeListFiles = modal._utils.grpc_utils.UnaryStreamWrapper(grpclib_stub.VolumeListFiles)
        self.VolumePutFiles = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.VolumePutFiles)
        self.VolumeReload = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.VolumeReload)
        self.VolumeRemoveFile = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.VolumeRemoveFile)
        self.WorkspaceNameLookup = modal._utils.grpc_utils.UnaryUnaryWrapper(grpclib_stub.WorkspaceNameLookup)
