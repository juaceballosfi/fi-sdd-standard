// Plantilla de fi-sdd-standard (ADR-0023). /project-context la copia al proyecto de pruebas y
// backend-dev la adapta: los cuatro marcadores {{...}} y, si hace falta, las listas de excepciones.
// Las reglas no se relajan: una excepción nueva se justifica en su comentario y se reduce con el
// tiempo, nunca crece sin decisión del tech lead.
//   {{TestNamespace}}     espacio de nombres del proyecto de pruebas (p. ej. Bonis.Tests)
//   {{AppMarkerType}}     un tipo público de la aplicación (p. ej. Program o un controller)
//   {{DataNamespace}}     espacio de nombres de la capa de datos (p. ej. Bonis.Data)
//   {{ServicesNamespace}} espacio de nombres de los servicios (p. ej. Bonis.Services)
using System.Reflection;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Xunit;

namespace {{TestNamespace}}.Architecture;

/// <summary>
/// Reglas de arquitectura del estándar: los controllers no usan el DbContext, todo endpoint
/// declara su autorización y la capa de datos no depende de los servicios.
/// </summary>
public class ArchitectureTests
{
    private static readonly Assembly App = typeof({{AppMarkerType}}).Assembly;

    // Controllers que todavía usan el DbContext directamente (deuda). Nombre de la clase y motivo.
    private static readonly HashSet<string> DbContextExceptions = [];

    // Controllers o acciones sin atributo de autorización a propósito (p. ej. un health check público).
    private static readonly HashSet<string> AuthorizationExceptions = [];

    private static IEnumerable<Type> Controllers() =>
        App.GetTypes().Where(t => t is { IsClass: true, IsAbstract: false } && typeof(ControllerBase).IsAssignableFrom(t));

    private static bool DeclaresAuthorization(MemberInfo member) =>
        member.GetCustomAttributes(inherit: true).Any(a => a.GetType().GetInterfaces()
            .Any(i => i.Name is "IAuthorizeData" or "IAllowAnonymous" or "IAuthorizationRequirementData"));

    [Fact]
    public void Los_controllers_no_dependen_del_DbContext()
    {
        var offenders = Controllers()
            .Where(c => !DbContextExceptions.Contains(c.Name))
            .Where(c => c.GetConstructors().SelectMany(k => k.GetParameters())
                .Any(p => typeof(DbContext).IsAssignableFrom(p.ParameterType)))
            .Select(c => c.FullName)
            .ToList();

        Assert.True(offenders.Count == 0, "Controllers que inyectan el DbContext: " + string.Join(", ", offenders));
    }

    [Fact]
    public void Todo_endpoint_declara_su_autorizacion()
    {
        var offenders = new List<string>();
        foreach (var controller in Controllers().Where(c => !AuthorizationExceptions.Contains(c.Name)))
        {
            if (DeclaresAuthorization(controller))
            {
                continue;
            }

            offenders.AddRange(controller.GetMethods(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly)
                .Where(m => !m.IsSpecialName && m.GetCustomAttribute<NonActionAttribute>() is null)
                .Where(m => !DeclaresAuthorization(m) && !AuthorizationExceptions.Contains($"{controller.Name}.{m.Name}"))
                .Select(m => $"{controller.Name}.{m.Name}"));
        }

        Assert.True(offenders.Count == 0, "Endpoints sin [Authorize] ni [AllowAnonymous]: " + string.Join(", ", offenders));
    }

    [Fact]
    public void La_capa_de_datos_no_depende_de_los_servicios()
    {
        const string data = "{{DataNamespace}}";
        const string services = "{{ServicesNamespace}}";

        static IEnumerable<Type> Used(Type t)
        {
            const BindingFlags all = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance |
                                     BindingFlags.Static | BindingFlags.DeclaredOnly;
            return t.GetFields(all).Select(f => f.FieldType)
                .Concat(t.GetProperties(all).Select(p => p.PropertyType))
                .Concat(t.GetConstructors(all).SelectMany(c => c.GetParameters()).Select(p => p.ParameterType))
                .Concat(t.GetMethods(all).SelectMany(m => m.GetParameters().Select(p => p.ParameterType).Append(m.ReturnType)))
                .SelectMany(u => u.IsGenericType ? u.GetGenericArguments().Append(u) : new[] { u });
        }

        var offenders = App.GetTypes()
            .Where(t => t.Namespace?.StartsWith(data, StringComparison.Ordinal) == true)
            .SelectMany(t => Used(t).Where(u => u.Namespace?.StartsWith(services, StringComparison.Ordinal) == true)
                .Select(u => $"{t.Name} → {u.Name}"))
            .Distinct()
            .ToList();

        Assert.True(offenders.Count == 0, "La capa de datos usa servicios: " + string.Join(", ", offenders));
    }
}
